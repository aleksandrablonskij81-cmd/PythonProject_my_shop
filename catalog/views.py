from django.shortcuts import render

def home(request):
    context = {
        'products': [
            {'name': 'Ноутбук', 'price': 1500, 'description': 'Мощный ноутбук'},
            {'name': 'Смартфон', 'price': 800, 'description': 'Современный смартфон'},
            {'name': 'Наушники', 'price': 200, 'description': 'Беспроводные наушники'},
        ]
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    context = {
        'email': 'shop@example.com',
        'phone': '+7 (999) 123-45-67',
        'address': 'г. Москва, ул. Тверская, д. 1'
    }
    return render(request, 'catalog/contacts.html', context)
