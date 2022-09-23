from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from products.models import Product
from account.models import User


@login_required
def wishlist(request):
    user = User.objects.get(request.id)
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'wishlist_detail.html',
                  {"wishlist": products,
                   'user': user})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user.id)
        messages.success(request, product.name + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user.id)
        messages.success(request, "Added " + product.name + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
