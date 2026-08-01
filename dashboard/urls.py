from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("appointments/", views.appointment_list, name="appointment_list"),
    path("appointments/<int:pk>/reply/", views.appointment_reply, name="appointment_reply"),
]
