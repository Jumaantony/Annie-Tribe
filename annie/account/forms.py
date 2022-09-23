from django.contrib.auth.forms import UserCreationForm
from django import forms

from phonenumber_field.formfields import PhoneNumberField

from .models import User


class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Format +254 742 490 000')
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone')


class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter Verification Code')


class UserEditForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, required=True, help_text='Format +254 742 490 000')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', )

