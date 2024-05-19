from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import IndexListView, ContactsView, ProductCreateView, ProductUpdateView, \
    ProductDetailView, ProductDeleteView, UpdateVersionView, CategoryListView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name="index"),
    path('contact/', ContactsView.as_view(), name="contact"),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('update_version/', UpdateVersionView.as_view(), name='update_version'),
    path('category/', CategoryListView.as_view(), name='category_list'),
]
