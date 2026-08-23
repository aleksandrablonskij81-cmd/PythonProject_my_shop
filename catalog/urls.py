from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
]