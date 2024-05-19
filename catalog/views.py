from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from catalog.models import Product, Version, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from django.forms import inlineformset_factory

from catalog.services import get_category_from_cache, get_products_from_cache


class IndexListView(ListView):
    model = Product
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_perms'] = self.request.user.groups.filter(name='moderator').exists()
        return context

    def get_queryset(self):
        return get_products_from_cache()


class CategoryListView(ListView):
    model = Category
    template_name = 'main/category_list.html'

    def get_queryset(self):
        return get_category_from_cache()


class ContactsView(TemplateView):
    template_name = 'main/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'main/product_list.html'


class ProductDetailView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.groups.filter(name='moderator').exists():
            self.object.save()
            return self.object
        return PermissionDenied


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'main/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'main/product_update.html'
    success_url = reverse_lazy('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1, can_delete=False)
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))

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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_cancel_published") and user.has_perm(
                "catalog.can_edit_description") and user.has_perm("catalog.can_edit_category"):
            return ProductModeratorForm
        raise PermissionDenied


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
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:index')

    def get_success_url(self):
        return reverse('catalog:index', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, VersionForm, extra=1, can_delete=False)
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
