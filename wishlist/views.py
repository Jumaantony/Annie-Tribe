from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .wishlist import Wishlist
from .forms import WishlistAddProductForm


@login_required
@require_POST
def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    form = WishlistAddProductForm(request.POST)
    if form.is_valid():
        wishlist.add(product=product)
    return redirect('wishlist:wishlist_detail')


@login_required
@require_POST
def wishlist_remove(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.remove(product)
    return redirect('wishlist:wishlist_detail')


@login_required
def wishlist_detail(request):
    wishlist = Wishlist(request)
    return render(request, 'wishlist_detail.html',
                  {'wishlist': wishlist})

