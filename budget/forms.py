from django import forms

from .models import BmsdBudget, BudgetUtilizeDistrict, ReviseBudgetDistrict


class BmsdBudgetForm(forms.ModelForm):
    class Meta:
        model = BmsdBudget
        fields = '__all__'


class BudgetUtilizeDistrictForm(forms.ModelForm):
    class Meta:
        model = BudgetUtilizeDistrict
        fields = '__all__'


class ReviseBudgetDistrictForm(forms.ModelForm):
    class Meta:
        model = ReviseBudgetDistrict
        fields = '__all__'