from django.shortcuts import render, get_object_or_404


# Create your views here.
from orders.models import OrderItem, Order
from cart.cart import Cart


def payment_options(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    ordered_items = OrderItem.objects.filter(order=order_id)

    # request for cart
    print(ordered_items)

    return render(request, 'payment_options.html',
                  {'order': order,
                   'ordered_items': ordered_items})
