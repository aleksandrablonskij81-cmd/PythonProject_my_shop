from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm


# Список товаров (доступен всем)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products})


# Детальный просмотр (доступен всем)
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


# Создание товара (только авторизованные)
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect('catalog:product_list')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})


# Редактирование (только владелец или модератор)
@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.owner != request.user and not request.user.has_perm('catalog.can_unpublish_product'):
        raise PermissionDenied('У вас нет прав на редактирование этого продукта')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('catalog:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalog/product_form.html', {'form': form})


# Удаление (только владелец или модератор)
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.owner != request.user and not request.user.has_perm('catalog.delete_product'):
        raise PermissionDenied('У вас нет прав на удаление этого продукта')

    if request.method == 'POST':
        product.delete()
        return redirect('catalog:product_list')
    return render(request, 'catalog/product_confirm_delete.html', {'product': product})


# Переключение публикации (только модератор)
@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def product_toggle_publish(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.is_published = not product.is_published
    product.save()
    return redirect('catalog:product_detail', pk=product.pk)