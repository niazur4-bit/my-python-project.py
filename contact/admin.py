from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "phone", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    list_editable = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
