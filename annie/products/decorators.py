from django.contrib.auth.decorators import user_passes_test

from orders.models import OrderItem


def product_purchase_delivered(f):
    ordered_items = OrderItem.objects.filter()
    return user_passes_test(lambda order_items: ordered_items.order.order_status)(f)
