from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ("tax", "Tax Updates"),
        ("secp", "SECP & Compliance"),
        ("audit", "Audit & Assurance"),
        ("news", "Firm News"),
        ("guides", "Guides"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="blog_posts")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="news")
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})
