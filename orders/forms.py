from django import forms
from django.contrib.auth.models import User
from .models import Order


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_number', 'county', 'town', 'address',
                  'postal_code']
