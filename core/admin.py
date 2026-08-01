from django.contrib import admin
from .models import Testimonial, FAQ, Document, TeamMember


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "designation", "rating", "is_active", "created_at")
    list_filter = ("is_active", "rating")
    list_editable = ("is_active",)
    search_fields = ("client_name", "content")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("question", "answer")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "uploaded_at")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "order", "is_active")
    list_editable = ("order", "is_active")
