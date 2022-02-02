from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',  'email',
                    'phone_number', 'county',
                    'town', 'address', 'postal_code', 'paid',
                    'order_status', 'created', 'updated']
    list_filter = ['order_status', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]
