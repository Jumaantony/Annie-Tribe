from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    # index page
    path('', views.index, name='index'),

    # list of all products
    path('products/', views.product_list, name='product_list'),

    # list of products in a given category
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    # product detail
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]