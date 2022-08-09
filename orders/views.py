from django.shortcuts import render, redirect
from django.urls import reverse

from .models import OrderItem, Order
from .forms import OrderCreateForm, UserEditForm
from cart.cart import Cart


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            print(request.user)
            for item in cart:
                OrderItem.objects.create(
                    user=request.user,
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])

            # # clear cart
            # cart.clear()
            return redirect(reverse('payment:payment_options'))
    else:
        order_form = OrderCreateForm()
    return render(request, 'create.html', {'cart': cart,
                                           'order_form': order_form, })


def order_list(request):
    orders = Order.objects.all()
    ordered_items = OrderItem.objects.filter(user=request.user)
    return render(request, 'orders.html',
                  {'orders': orders,
                   'ordered_items': ordered_items})
