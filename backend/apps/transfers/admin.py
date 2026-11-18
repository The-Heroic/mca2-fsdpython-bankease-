from django.contrib import admin
from .models import Beneficiary, Transaction

admin.site.register(Beneficiary)
admin.site.register(Transaction)
