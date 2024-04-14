from catalog.models import Product
from django.views.generic import ListView, TemplateView, DetailView


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
    template_name = 'main/product.html'


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
