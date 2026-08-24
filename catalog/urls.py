from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add/', views.ProductCreateView.as_view(), name='add_product'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),  # если есть
]