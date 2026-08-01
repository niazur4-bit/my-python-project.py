from django.contrib.sitemaps import Sitemap
from blog.models import BlogPost
from services.models import Service


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
