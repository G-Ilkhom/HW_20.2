from django.urls import path
from catalog.views import IndexListView, ContactsView, ProductListView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name="index"),
    path('product/', ProductListView.as_view(), name="product"),
    path('contact/', ContactsView.as_view(), name="contact"),
]
