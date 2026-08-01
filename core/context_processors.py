from django.conf import settings


def site_settings(request):
    """Makes site-wide branding/SEO values available in every template."""
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
    }
