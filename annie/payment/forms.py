from django import forms


class MpesaPhoneForm(forms.Form):
    phone = forms.CharField(help_text='format: 254 742 XXX XXX')
