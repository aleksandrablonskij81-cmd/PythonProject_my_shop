from django import forms
from .models import Product

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


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

    def __init__(self, *args, **kwargs):
        """Добавляем стили для всех полей"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ in [forms.TextInput, forms.NumberInput, forms.Textarea, forms.Select]:
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'description':
                field.widget.attrs['rows'] = 5
            if field_name == 'price':
                field.widget.attrs['step'] = '0.01'

    def clean_name(self):
        """Валидация названия — проверка на запрещенные слова"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for word in FORBIDDEN_WORDS:
                if word in name_lower:
                    raise forms.ValidationError(
                        f'Название содержит запрещенное слово: "{word}"'
                    )
        return name

    def clean_description(self):
        """Валидация описания — проверка на запрещенные слова"""
        description = self.cleaned_data.get('description')
        if description:
            description_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(
                        f'Описание содержит запрещенное слово: "{word}"'
                    )
        return description

    def clean_price(self):
        """Валидация цены — не может быть отрицательной"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена не может быть отрицательной. Пожалуйста, введите положительное число.'
            )
        return price
