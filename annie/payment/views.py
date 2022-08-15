from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
import braintree
from orders.models import OrderItem, Order
from django.conf import settings

# Create your views here.
# instantiating braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


@login_required
def payment_options(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    ordered_items = OrderItem.objects.filter(order=order_id)

    return render(request, 'payment_options.html',
                  {'order': order,
                   'ordered_items': ordered_items})


@login_required
def card_payment(request):
    order_id = request.session.get('order_id')
    order = Order.objects.get(id=order_id)
    ordered_items = OrderItem.objects.filter(order=order_id)
    total_cost_after_discount = order.get_total_cost_after_discount()

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)

        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost_after_discount:.2f}',
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })

        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store unique transaction id
            order.braintree_id = result.transaction.id
            order.save()

            return redirect('payment:payment_done')
        else:
            return redirect('payment:payment_canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()

    return render(request, 'card.html',
                  {'order': order,
                   'ordered_items': ordered_items,
                   'total_cost_after_discount': total_cost_after_discount,
                   'client_token': client_token})


@login_required
def payment_done(request):
    return render(request, 'payment_done.html')


@login_required
def payment_canceled(request):
    return render(request, 'payment_canceled.html')
