from django import forms
from phonenumber_field.formfields import PhoneNumberField


class MpesaPhoneForm(forms.Form):
    phone = forms.CharField(help_text='format: 254 742 XXX XXX')
