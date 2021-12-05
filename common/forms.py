from django import forms

from .models import UserProfile, District


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'