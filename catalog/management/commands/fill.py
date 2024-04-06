from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': "Electronics"},
            {'name': "Clothing"},
            {'name': "Books"},
            {'name': "Toys"},
            {'name': "Furniture"},
        ]

        category_for_create = []
        for category_item in category_list:
            category_for_create.append(Category(**category_item))

        Category.objects.bulk_create(category_for_create)

        first_category = Category.objects.first()

        product_list = [
            {
                "name": "Laptop",
                "description": "",
                "image": "",
                "category": first_category,
                "price": "999.99",
                "created_at": "2024-04-06T17:53:39.341Z",
                "updated_at": "2024-04-06T17:53:39.341Z",
                "manufactured_at": "2024-04-06"
            }
        ]

        product_for_create = []
        for product_item in product_list:
            product_for_create.append(Product(**product_item))

        Product.objects.bulk_create(product_for_create)
