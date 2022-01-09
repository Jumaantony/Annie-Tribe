from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart(object):
    def __int__(self, request):