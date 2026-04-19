# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'role', 'is_verified', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'is_verified', 'student_id', 'course')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)