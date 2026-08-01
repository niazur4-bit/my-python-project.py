from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.utils import timezone

from .models import Appointment, AppointmentDocument


class AppointmentDocumentInline(admin.TabularInline):
    model = AppointmentDocument
    extra = 0
    fields = ("file", "note", "uploaded_by", "uploaded_at")
    readonly_fields = ("uploaded_at",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "preferred_date", "preferred_time", "status", "phone", "reply_status", "created_at")
    list_filter = ("status", "service", "preferred_date")
    list_editable = ("status",)
    search_fields = ("name", "email", "phone")
    date_hierarchy = "preferred_date"
    inlines = [AppointmentDocumentInline]
    fieldsets = (
        ("Client Info", {"fields": ("user", "name", "email", "phone")}),
        ("Appointment", {"fields": ("service", "preferred_date", "preferred_time", "message")}),
        ("Office Use", {"fields": ("status", "admin_notes")}),
        ("Reply to Client", {"fields": ("admin_reply", "replied_at"), "description": "Visible to the client on their account. Leave admin_notes above for internal-only remarks."}),
    )
    readonly_fields = ("replied_at",)

    @admin.display(boolean=True, description="Replied")
    def reply_status(self, obj):
        return obj.has_reply

    def save_model(self, request, obj, form, change):
        reply_changed = "admin_reply" in form.changed_data and obj.admin_reply
        if reply_changed:
            obj.replied_at = timezone.now()
        super().save_model(request, obj, form, change)
        if reply_changed:
            try:
                send_mail(
                    subject=f"Reply to your appointment request - {obj.service}",
                    message=(
                        f"Dear {obj.name},\n\n"
                        f"Munib and Co has replied to your appointment request for "
                        f"{obj.service} on {obj.preferred_date} at {obj.preferred_time}:\n\n"
                        f"{obj.admin_reply}\n\n"
                        f"You can view this reply anytime by logging into your account.\n\n"
                        f"Regards,\nMunib and Co"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[obj.email],
                    fail_silently=True,
                )
            except Exception:
                pass
