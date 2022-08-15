from django.urls import path, include
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment_options/', views.payment_options, name='payment_options'),

    path('card_payment/', views.card_payment, name='card_payment'),

    path('payment_done/', views.payment_done, name='payment_done'),

    path('payment_canceled', views.payment_canceled, name='payment_canceled'),
]
