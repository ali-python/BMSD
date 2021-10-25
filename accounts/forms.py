from django import forms

from .models import AccountLedger


class AccountLedgerForm(forms.ModelForm):
    class Meta:
        model = AccountLedger
        fields = '__all__'