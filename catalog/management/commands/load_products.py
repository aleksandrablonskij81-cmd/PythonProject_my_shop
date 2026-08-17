from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Загружает тестовые продукты'

    def handle(self, *args, **options):
        # Удаляем старые данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write('✅ Старые данные удалены')

        # Создаём категории
        categories = [
            {'name': 'Электроника', 'description': 'Техника и гаджеты'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
            {'name': 'Книги', 'description': 'Художественная литература'},
        ]

        for cat_data in categories:
            Category.objects.create(
                name=cat_data['name'],
                description=cat_data['description']
            )
            self.stdout.write(f'  ✅ Создана категория: {cat_data["name"]}')

        # Создаём продукты
        products = [
            {'name': 'Ноутбук', 'description': 'Мощный ноутбук', 'price': 1500.00, 'category': 'Электроника'},
            {'name': 'Смартфон', 'description': 'Современный смартфон', 'price': 800.00, 'category': 'Электроника'},
            {'name': 'Наушники', 'description': 'Беспроводные наушники', 'price': 200.00, 'category': 'Электроника'},
            {'name': 'Футболка', 'description': 'Хлопковая футболка', 'price': 25.00, 'category': 'Одежда'},
            {'name': 'Джинсы', 'description': 'Классические джинсы', 'price': 50.00, 'category': 'Одежда'},
            {'name': 'Война и мир', 'description': 'Роман Толстого', 'price': 15.00, 'category': 'Книги'},
        ]

        for prod_data in products:
            category = Category.objects.get(name=prod_data['category'])
            Product.objects.create(
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                category=category
            )
            self.stdout.write(f'  ✅ Создан продукт: {prod_data["name"]}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Загружено {Product.objects.count()} продуктов в {Category.objects.count()} категориях'
            )
        )
