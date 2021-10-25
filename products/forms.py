from django import forms

from .models import Company, Product, StockIn,StockOut, ProductDetail, PurchasedProduct


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = '__all__'

class StockOutForm(forms.ModelForm):
    class Meta:
        model = StockOut
        fields = '__all__'

class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = '__all__'