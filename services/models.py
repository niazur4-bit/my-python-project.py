from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Service(models.Model):
    ICON_CHOICES = [
        ("bi-receipt", "Receipt"),
        ("bi-cash-coin", "Cash"),
        ("bi-building", "Building"),
        ("bi-card-checklist", "Checklist"),
        ("bi-journal-text", "Journal"),
        ("bi-search", "Audit / Search"),
        ("bi-shield-check", "Compliance"),
        ("bi-people", "Consultancy"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    icon = models.CharField(max_length=40, choices=ICON_CHOICES, default="bi-receipt")
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    fee_note = models.CharField(max_length=150, blank=True, help_text="e.g. 'Starting from PKR 5,000'")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})
