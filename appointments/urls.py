from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [
    path("book/", views.book_appointment, name="book"),
    path("my-appointments/", views.my_appointments, name="my_appointments"),
    path("<int:pk>/", views.appointment_detail, name="detail"),
    path("documents/<int:pk>/download/", views.document_download, name="document_download"),
]
