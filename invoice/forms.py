from django import forms

from .models import Invoice, InvoiceNotification


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceNotificationForm(forms.ModelForm):
    class Meta:
        model = InvoiceNotification
        fields = '__all__'