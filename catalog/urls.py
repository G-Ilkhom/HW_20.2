from django.urls import path
from catalog.views import IndexListView, ContactsView, ProductListView, ProductCreateView, ProductUpdateView, \
    ProductDetailView, ProductDeleteView, UpdateVersionView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name="index"),
    path('contact/', ContactsView.as_view(), name="contact"),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('update_version/', UpdateVersionView.as_view(), name='update_version'),
]
