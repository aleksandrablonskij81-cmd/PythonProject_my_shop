from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from .models import Product, Category
from .forms import ProductForm
from .services import get_products_by_category, get_category


# ===== СПИСОК ТОВАРОВ (Задание 4 — низкоуровневое кеширование) =====
def product_list(request):
    cache_key = 'product_list_all'
    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.all())
        cache.set(cache_key, products, 60 * 15)  # 15 минут

    return render(request, 'catalog/product_list.html', {'products': products})


# ===== ДЕТАЛЬНЫЙ ПРОСМОТР (Задание 2 — кеширование страницы) =====
def product_detail(request, pk):
    cache_key = f'product_detail_{pk}'
    product = cache.get(cache_key)

    if product is None:
        product = get_object_or_404(Product, id=pk)
        cache.set(cache_key, product, 60 * 30)  # 30 минут

    return render(request, 'catalog/product_detail.html', {'product': product})


# ===== СОЗДАНИЕ ТОВАРА =====
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            # Сбрасываем кеш после создания товара
            cache.delete('product_list_all')
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})


# ===== РЕДАКТИРОВАНИЕ (владелец или модератор) =====
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
        raise PermissionDenied('У вас нет прав на редактирование этого продукта')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Сбрасываем кеш после редактирования
            cache.delete(f'product_detail_{pk}')
            cache.delete('product_list_all')
            cache.delete(f'category_{product.category_id}')
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})


# ===== УДАЛЕНИЕ (владелец или модератор) =====
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
        raise PermissionDenied('У вас нет прав на удаление этого продукта')

    if request.method == 'POST':
        category_id = product.category_id
        product.delete()
        # Сбрасываем кеш
        cache.delete('product_list_all')
        cache.delete(f'category_{category_id}')
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})


# ===== ПЕРЕКЛЮЧЕНИЕ ПУБЛИКАЦИИ (модератор) =====
@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def product_toggle_publish(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.is_published = not product.is_published
    product.save()
    # Сбрасываем кеш
    cache.delete(f'product_detail_{pk}')
    cache.delete('product_list_all')
    return redirect('catalog:product_detail', pk=product.pk)


# ===== СПИСОК ТОВАРОВ ПО КАТЕГОРИИ (Задание 3) =====
def products_by_category(request, category_id):
    """
    Представление: список всех продуктов в указанной категории.
    Использует сервисную функцию с кешированием.
    """
    category = get_category(category_id)

    if category is None:
        return render(request, 'catalog/category_not_found.html', status=404)

    products = get_products_by_category(category_id)

    context = {
        'category': category,
        'products': products,
    }

    return render(request, 'catalog/products_by_category.html', context)