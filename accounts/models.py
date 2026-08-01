from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """Custom user model. Every account is either a client or a staff/admin
    member (staff members are managed via is_staff / is_superuser)."""

    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    cnic = models.CharField("CNIC", max_length=20, blank=True, help_text="National ID number")
    company_name = models.CharField(max_length=150, blank=True)
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.get_full_name() or self.username

    def get_absolute_url(self):
        return reverse("accounts:profile")
