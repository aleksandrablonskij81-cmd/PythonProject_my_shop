from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category  # импортируйте ваши модели
from .forms import ProductForm  # если есть форма

# 👇 ЭТА ФУНКЦИЯ ОТВЕЧАЕТ ЗА СПИСОК ТОВАРОВ (ГЛАВНАЯ СТРАНИЦА)
def product_list(request):
    products = Product.objects.all()  # получаем все товары
    return render(request, 'catalog/product_list.html', {'products': products})

# 👇 ЭТА ФУНКЦИЯ ОТВЕЧАЕТ ЗА ДЕТАЛЬНЫЙ ПРОСМОТР ТОВАРА
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

# 👇 ЭТА ФУНКЦИЯ ОТВЕЧАЕТ ЗА СОЗДАНИЕ ТОВАРА
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})

# 👇 ЭТА ФУНКЦИЯ ОТВЕЧАЕТ ЗА РЕДАКТИРОВАНИЕ ТОВАРА
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})

# 👇 ЭТА ФУНКЦИЯ ОТВЕЧАЕТ ЗА УДАЛЕНИЕ ТОВАРА
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})