from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm, UserEditForm
from cart.cart import Cart


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid() and user_form.is_valid():
            user_form.save()
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            # clear cart
            cart.clear()
            return render(request, 'created.html',
                          {'order': order, })
    else:
        order_form = OrderCreateForm()
        user_form = UserEditForm(instance=request.user)
    return render(request, 'create.html', {'cart': cart,
                                           'order_form': order_form,
                                           'user_form': user_form, })
