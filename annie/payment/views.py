from django.shortcuts import render, get_object_or_404


# Create your views here.
from orders.models import OrderItem, Order


def payment_options(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    # order = Order.objects.all()
    # ordered_items = OrderItem.objects.filter(user=request.user)

    print(ordered_items)

    return render(request, 'payment_options.html',
                  {'ordered_items ': ordered_items,
                   'order': order})
