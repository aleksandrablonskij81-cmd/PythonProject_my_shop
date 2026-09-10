from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id):
    """
    Сервисная функция: возвращает список всех продуктов в указанной категории.
    Использует низкоуровневое кеширование с ключом category_{id} и TTL 15 минут.
    """
    cache_key = f'category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        # Проверяем, существует ли категория
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return None

        # Получаем продукты в этой категории
        products = list(Product.objects.filter(category=category))

        # Сохраняем в кеш на 15 минут
        cache.set(cache_key, products, 60 * 15)

    return products


def get_category(category_id):
    """
    Возвращает объект категории по ID (с кешированием на 30 минут).
    """
    cache_key = f'category_obj_{category_id}'
    category = cache.get(cache_key)

    if category is None:
        try:
            category = Category.objects.get(id=category_id)
            cache.set(cache_key, category, 60 * 30)
        except Category.DoesNotExist:
            return None

    return category