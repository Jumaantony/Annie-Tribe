from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_options/', views.payment_options, name='payment_options'),

    path('card_payment/', views.card_payment, name='card_payment'),

    path('access/token', views.get_access_token, name='get_mpesa_access_token'),

    path('mpesa_payment/', views.mpesa_payment, name='mpesa_payment'),

    # register, confirmation, validation and callback urls
    path('register_mpesa_validation/', views.register_urls, name="register_mpesa_validation"),
    path('confirmation/', views.confirmation, name="confirmation"),
    path('validation/', views.validation, name="validation"),
    path('callback/', views.call_back, name="call_back"),

    path('payment_done/', views.payment_done, name='payment_done'),

    path('payment_canceled', views.payment_canceled, name='payment_canceled'),
]
