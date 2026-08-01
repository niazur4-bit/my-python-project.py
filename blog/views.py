from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True, published_at__lte=timezone.now())
    category = request.GET.get("category")
    if category:
        posts = posts.filter(category=category)
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/blog_list.html", {
        "page_obj": page_obj,
        "categories": BlogPost.CATEGORY_CHOICES,
        "active_category": category,
    })


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:4]
    return render(request, "blog/blog_detail.html", {"post": post, "recent_posts": recent_posts})
