from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import timedelta

from appointments.models import Appointment, AppointmentDocument
from blog.models import BlogPost
from contact.models import ContactMessage
from core.models import Testimonial
from services.models import Service

from appointments.forms import AppointmentDocumentForm
from .forms import AppointmentReplyForm

User = get_user_model()


def staff_check(user):
    return user.is_active and user.is_staff


@user_passes_test(staff_check, login_url="accounts:login")
def index(request):
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)

    context = {
        "client_count": User.objects.filter(is_staff=False).count(),
        "new_clients_30d": User.objects.filter(is_staff=False, created_at__date__gte=last_30_days).count(),
        "service_count": Service.objects.filter(is_active=True).count(),
        "appointment_count": Appointment.objects.count(),
        "pending_appointments": Appointment.objects.filter(status="pending").count(),
        "confirmed_appointments": Appointment.objects.filter(status="confirmed").count(),
        "upcoming_appointments": Appointment.objects.filter(preferred_date__gte=today, status__in=["pending", "confirmed"]).order_by("preferred_date")[:8],
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "total_messages": ContactMessage.objects.count(),
        "recent_messages": ContactMessage.objects.all()[:6],
        "blog_count": BlogPost.objects.filter(is_published=True).count(),
        "testimonial_count": Testimonial.objects.filter(is_active=True).count(),
    }
    return render(request, "dashboard/index.html", context)


@user_passes_test(staff_check, login_url="accounts:login")
def appointment_list(request):
    appointments = Appointment.objects.select_related("service", "user").all()

    status = request.GET.get("status")
    if status:
        appointments = appointments.filter(status=status)

    reply_filter = request.GET.get("reply")
    if reply_filter == "pending":
        appointments = appointments.exclude(admin_reply__gt="").filter(admin_reply="")
    elif reply_filter == "replied":
        appointments = appointments.exclude(admin_reply="")

    context = {
        "appointments": appointments,
        "status": status,
        "reply_filter": reply_filter,
        "status_choices": Appointment.STATUS_CHOICES,
    }
    return render(request, "dashboard/appointment_list.html", context)


@user_passes_test(staff_check, login_url="accounts:login")
def appointment_reply(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == "POST" and request.POST.get("form_name") == "document":
        doc_form = AppointmentDocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save(commit=False)
            doc.appointment = appointment
            doc.uploaded_by = request.user
            doc.save()

            try:
                send_mail(
                    subject=f"A document has been shared with you - {appointment.service}",
                    message=(
                        f"Dear {appointment.name},\n\n"
                        f"Munib and Co has shared a document with you "
                        f"(\"{doc.note or doc.filename}\") for your appointment on "
                        f"{appointment.preferred_date}.\n\n"
                        f"Log in to your account under \"My Appointments\" to view and download it.\n\n"
                        f"Regards,\nMunib and Co"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appointment.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Document uploaded and the client has been notified.")
            return redirect("dashboard:appointment_reply", pk=appointment.pk)
        reply_form = AppointmentReplyForm(instance=appointment)

    elif request.method == "POST":
        previous_reply = appointment.admin_reply
        reply_form = AppointmentReplyForm(request.POST, instance=appointment)
        doc_form = AppointmentDocumentForm()
        if reply_form.is_valid():
            reply_text = reply_form.cleaned_data["admin_reply"]
            reply_is_new_or_changed = bool(reply_text) and reply_text != previous_reply
            appt = reply_form.save(commit=False)
            if reply_is_new_or_changed:
                appt.replied_at = timezone.now()
            appt.save()

            if reply_is_new_or_changed:
                try:
                    send_mail(
                        subject=f"Reply to your appointment request - {appt.service}",
                        message=(
                            f"Dear {appt.name},\n\n"
                            f"Munib and Co has replied to your appointment request for "
                            f"{appt.service} on {appt.preferred_date} at {appt.preferred_time}:\n\n"
                            f"{appt.admin_reply}\n\n"
                            f"You can view this reply anytime by logging into your account "
                            f"under \"My Appointments\".\n\n"
                            f"Regards,\nMunib and Co"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[appt.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            messages.success(request, f"Your reply to {appt.name} has been saved and emailed to the client.")
            return redirect("dashboard:appointment_list")
    else:
        reply_form = AppointmentReplyForm(instance=appointment)
        doc_form = AppointmentDocumentForm()

    return render(request, "dashboard/appointment_reply.html", {
        "form": reply_form,
        "doc_form": doc_form,
        "appointment": appointment,
        "documents": appointment.documents.all(),
    })
