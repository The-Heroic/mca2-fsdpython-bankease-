from django.contrib import admin
from .models import BillerDirectory, BillPayment, CustomerBiller

admin.site.register(BillerDirectory)
admin.site.register(CustomerBiller)
admin.site.register(BillPayment)
