from django.contrib import admin
from django.contrib.auth.admin import Group, UserAdmin as BaseUserAdmin
from .models import User, Clients
from .models import Clients


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'telegram_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'telegram_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Clients)
