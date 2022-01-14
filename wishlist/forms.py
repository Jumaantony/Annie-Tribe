from django import forms


class WishlistAddProductForm(forms.Form):
    quantity = int(1)
