from django.core.cache import cache

from config.settings import CACHE_ENABLED
from catalog.models import Category, Product


def get_category_from_cache():
    """Получает данные по категориям из кэша, если кэш пуст, получает данные из бд."""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = "category_list"
    category = cache.get(key)
    if category is not None:
        return category
    category = Category.objects.all()
    cache.set(key, category)
    return category


def get_products_from_cache():
    """Получает данные по продуктам из кэша, если кэш пуст, получает данные из бд."""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    product = cache.get(key)
    if product is not None:
        return product
    product = Product.objects.all()
    cache.set(key, product)
    return product
