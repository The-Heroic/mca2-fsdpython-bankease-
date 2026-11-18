from django.contrib import admin
from .models import LoanApplication, LoanProduct, LoanRepayment

admin.site.register(LoanProduct)
admin.site.register(LoanApplication)
admin.site.register(LoanRepayment)
