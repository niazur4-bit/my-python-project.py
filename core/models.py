from django.db import models


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    designation = models.CharField(max_length=150, blank=True, help_text="e.g. 'CEO, Swat Textiles'")
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="1 to 5 stars")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} ({self.rating}*)"

    def stars_range(self):
        return range(self.rating)

    def empty_stars_range(self):
        return range(5 - self.rating)


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Document(models.Model):
    CATEGORY_CHOICES = [
        ("income_tax", "Income Tax Forms"),
        ("sales_tax", "Sales Tax Forms"),
        ("secp", "SECP / Incorporation"),
        ("checklist", "Client Checklists"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    description = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "title"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    designation = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
