from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core.sitemaps import ServiceSitemap, BlogSitemap

sitemaps = {"services": ServiceSitemap, "blog": BlogSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("appointments/", include("appointments.urls")),
    path("blog/", include("blog.urls")),
    path("contact/", include("contact.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
