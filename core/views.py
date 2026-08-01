from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from blog.models import BlogPost
from services.models import Service
from .models import Testimonial, FAQ, Document, TeamMember


def home(request):
    context = {
        "services": Service.objects.filter(is_active=True)[:8],
        "testimonials": Testimonial.objects.filter(is_active=True)[:6],
        "posts": BlogPost.objects.filter(is_published=True)[:3],
    }
    return render(request, "core/home.html", context)


def about(request):
    team = TeamMember.objects.filter(is_active=True)
    return render(request, "core/about.html", {"team": team})


def faq_list(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, "core/faq.html", {"faqs": faqs})


def documents_list(request):
    documents = Document.objects.all()
    category = request.GET.get("category")
    if category:
        documents = documents.filter(category=category)
    return render(request, "core/documents.html", {
        "documents": documents,
        "categories": Document.CATEGORY_CHOICES,
        "active_category": category,
    })


def search(request):
    query = request.GET.get("q", "").strip()
    services = blog_posts = []
    if query:
        services = Service.objects.filter(
            Q(is_active=True) & (Q(title__icontains=query) | Q(short_description__icontains=query) | Q(description__icontains=query))
        )
        blog_posts = BlogPost.objects.filter(
            Q(is_published=True) & (Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))
        )
    return render(request, "core/search_results.html", {
        "query": query,
        "services": services,
        "blog_posts": blog_posts,
        "result_count": len(services) + len(blog_posts),
    })


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /dashboard/",
        "Disallow: /accounts/dashboard/",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
