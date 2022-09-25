from django.contrib import admin
from .models import MpesaPayment

# Register your models here.
admin.site.register(MpesaPayment)


class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'description',
                    'phone_number', 'amount', 'reference', 'organization_balance',
                    'type',
                    ]
