from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, \
    MaxValueValidator

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from coupons.models import Coupon


# Create your models here.
class Order(models.Model):
    order_status_choices = (
        ('Pending', 'Pending'),
        ('En_route', 'En_route'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = PhoneNumberField()
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    order_status = models.CharField(max_length=10,
                                    choices=order_status_choices,
                                    default='Pending', )
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    braintree_id = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost

    def get_total_cost_after_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - round(total_cost * (self.discount / Decimal(100)), 2)


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)

    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
