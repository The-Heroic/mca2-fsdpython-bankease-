from django.contrib import admin
from .models import Branch, Role, User

admin.site.register(Role)
admin.site.register(Branch)
admin.site.register(User)
