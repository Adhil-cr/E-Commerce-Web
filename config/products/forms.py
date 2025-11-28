from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'product_image', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Product title, e.g. Logitech MX Master 3'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': 'Price in ₹'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea-field',
                'placeholder': 'Short product description',
                'rows': 5
            }),
            'priority': forms.NumberInput(attrs={
                'class': 'input-field',
                'placeholder': 'Priority (higher shows first)'
            }),
            # product_image will be handled by the template file input; giving it a class helps
            'product_image': forms.FileInput(attrs={
                'class': 'file-input'
            }),
        }
