from django.contrib import admin
from .models import KYCDocument, SecurityAuditLog

admin.site.register(KYCDocument)
admin.site.register(SecurityAuditLog)
