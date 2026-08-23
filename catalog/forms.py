from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Введите описание товара...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Введите название...'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Введите цену...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'category': 'Категория',
            'price': 'Цена (руб.)',
            'image': 'Изображение',
        }