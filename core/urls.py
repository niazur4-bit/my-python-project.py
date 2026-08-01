from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq_list, name="faq"),
    path("documents/", views.documents_list, name="documents"),
    path("search/", views.search, name="search"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
