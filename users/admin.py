from django.contrib import admin

from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active', 'phone_number', 'is_staff', 'birthdate')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
