from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "fee_note", "order", "is_active", "updated_at")
    list_filter = ("is_active",)
    list_editable = ("order", "is_active")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
