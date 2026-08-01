from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "is_published", "published_at")
    list_filter = ("category", "is_published")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)
