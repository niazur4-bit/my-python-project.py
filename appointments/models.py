from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage
import os

from services.models import Service

import os as _os


class PrivateDocumentStorage(FileSystemStorage):
    """FileSystemStorage that always reads PRIVATE_MEDIA_ROOT from settings at
    access time (rather than freezing it at instantiation), so it responds
    correctly to override_settings in tests and to any settings reload."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", None)
        super().__init__(*args, **kwargs)

    @property
    def base_location(self):
        return settings.PRIVATE_MEDIA_ROOT

    @property
    def location(self):
        return _os.path.abspath(self.base_location)


# Documents are stored outside MEDIA_ROOT (see PRIVATE_MEDIA_ROOT in settings.py) so
# they can only ever be retrieved through the permission-checked download view, never
# by guessing a public /media/ URL.
private_document_storage = PrivateDocumentStorage()


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name="appointments")
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_notes = models.TextField(blank=True, help_text="Internal notes, not visible to client")
    admin_reply = models.TextField(blank=True, help_text="Reply from staff, visible to the client on their account")
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-preferred_date", "-preferred_time"]

    def __str__(self):
        return f"{self.name} - {self.service} ({self.preferred_date})"

    @property
    def has_reply(self):
        return bool(self.admin_reply)


class AppointmentDocument(models.Model):
    """A file shared between a client and staff for a specific appointment.
    Either side can upload one (e.g. client uploads a CNIC copy or bank
    statement; staff uploads the completed return or a receipt)."""

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="uploaded_appointment_documents",
    )
    file = models.FileField(upload_to="appointment_documents/%Y/%m/", storage=private_document_storage)
    note = models.CharField(max_length=255, blank=True, help_text="e.g. 'CNIC copy', 'Completed tax return'")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.filename} ({self.appointment})"

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def uploaded_by_staff(self):
        return bool(self.uploaded_by_id and self.uploaded_by and self.uploaded_by.is_staff)
