from django import forms
from .models import Review


class EmailForm(forms.Form):
    email = forms.EmailField()


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body',)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
