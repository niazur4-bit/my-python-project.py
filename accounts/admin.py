from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff", "is_active", "created_at")
    list_filter = ("is_staff", "is_active", "created_at")
    search_fields = ("username", "email", "first_name", "last_name", "phone", "company_name")
    fieldsets = UserAdmin.fieldsets + (
        ("Client Details", {"fields": ("phone", "address", "cnic", "company_name", "profile_photo")}),
    )
