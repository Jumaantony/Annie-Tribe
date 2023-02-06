from django.urls import path, include
from . import views

app_name = 'wishlist'

urlpatterns = [
    path("", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="add_to_wishlist"),
]
