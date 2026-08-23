from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Category
from .forms import ProductForm


def index(request):
    """Главная страница со списком товаров"""
    products_list = Product.objects.all().order_by('-created_at')

    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products_list = products_list.filter(category_id=category_id)

    # Пагинация
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'catalog/index.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })


def product_detail(request, pk):
    """Страница с подробной информацией о товаре"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    """Страница добавления нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:index')
    else:
        form = ProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})
