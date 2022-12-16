from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

# Create your views here.


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            user = request.user

            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount

            order.sub_total = Decimal(cart.get_total_price())
            order.total = Decimal(cart.get_total_price_after_discount())

            order.first_name = user.first_name
            order.last_name = user.last_name
            order.email = user.email
            order.phone_number = user.phone

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])

            # clear cart
            cart.clear()

            # set the order in the session
            request.session['order_id'] = order.id

            return redirect(reverse('payment:payment_options'))
    else:
        order_form = OrderCreateForm()
    return render(request, 'create.html', {'cart': cart,
                                           'order_form': order_form, })


@login_required
def order_list(request):
    orders = Order.objects.all()
    ordered_items = OrderItem.objects.filter(user=request.user.pk)
    return render(request, 'orders.html',
                  {'orders': orders,
                   'ordered_items': ordered_items})
