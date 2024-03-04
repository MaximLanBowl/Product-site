from django import forms
from django.core import validators
from .models import Product, Order
from django.forms import ModelForm
from django.contrib.auth.models import Group
from shopapp.models import Product


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={"Multiple": True}), )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_adress", "promocode", "user", "products"


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()