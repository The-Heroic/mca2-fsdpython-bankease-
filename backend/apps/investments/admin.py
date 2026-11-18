from django.contrib import admin
from .models import Investment, InvestmentPlan

admin.site.register(InvestmentPlan)
admin.site.register(Investment)
