from django.urls import path
from catalog.views import index, contact, product
from catalog.apps import CatalogConfig


app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name="index"),
    path('product/', product, name="product"),
    path('contact/', contact, name="contact"),
]