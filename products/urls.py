from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    # newsletter urls
    path('subscribe', views.subscribe_view, name='subscribe'),

    path('success/', views.subscribe_success_view, name='subscribe_success'),

    path('fail/', views.subscribe_fail_view, name='subscribe_fail'),

    path('unsubscribe/', views.unsubscribe_view, name='unsubscribe'),

    path('unsubscribe/success/', views.unsubscribe_success_view, name='unsubscribe_success'),

    path('unsubscribe/fail/', views.unsubscribe_fail_view, name='unsubscribe_fail'),

    # index page
    path('', views.index, name='index'),

    path('contact/', views.contact, name='contact'),

    # list of all products
    path('products/', views.product_list, name='product_list'),

    path('search/', views.search, name='search'),

    # list of products in a given category
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # product detail
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

]
