from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payment_options, name='payment_options'),
]
