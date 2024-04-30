from catalog.models import Product, Version
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from catalog.forms import ProductForm, VersionForm


class IndexListView(ListView):
    model = Product
    template_name = 'main/home.html'


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'main/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_update.html'
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_version = Version.objects.filter(product=self.object, is_current_version=True).first()
        initial_data = {}  # Add any initial data you want to prepopulate in the VersionForm
        version_form = VersionForm(instance=active_version, initial=initial_data)
        context['version_form'] = version_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        version_form = VersionForm(request.POST)
        if version_form.is_valid():
            version_instance = version_form.save(commit=False)
            version_instance.product = self.object
            version_instance.save()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def product_update(request, product_id):
        product = Product.objects.get(pk=product_id)
        if request.method == 'POST':
            product_form = ProductForm(request.POST, instance=product)
            version_form = VersionForm(request.POST)
            if product_form.is_valid() and version_form.is_valid():
                new_version = version_form.save(commit=False)
                new_version.product = product
                new_version.save()
                return redirect('home')
        else:
            product_form = ProductForm(instance=product)
            version_form = VersionForm()

        return render(request, 'main/product_update.html',
                      {'product': product, 'product_form': product_form, 'version_form': version_form})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
    template_name = 'main/product_confirm_delete.html'


class DeleteVersionView(View):
    def post(self, request, *args, **kwargs):
        version_id = request.POST.get('delete_version')
        version = get_object_or_404(Version, pk=version_id)
        if version.is_current_version:
            version.delete()
        return redirect('catalog:index')


class UpdateVersionView(View):
    def post(self, request, *args, **kwargs):
        if 'delete_version' in request.POST:
            # Логика удаления выбранной версии
            version_id = request.POST['version_id']
            Version.objects.get(id=version_id).delete()
        else:
            form = VersionForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['is_current_version']:
                    existing_current_version = Version.objects.filter(is_current_version=True).first()
                    if existing_current_version:
                        existing_current_version.is_current_version = False
                        existing_current_version.save()
                new_version = form.save()
        return redirect('home')  # Перенаправляем на главную страницу после обработки запроса
