from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import AppointmentForm, AppointmentDocumentForm
from .models import Appointment, AppointmentDocument


def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.is_authenticated:
                appointment.user = request.user
            appointment.save()

            try:
                send_mail(
                    subject=f"New appointment request - {appointment.service}",
                    message=(
                        f"Name: {appointment.name}\n"
                        f"Email: {appointment.email}\n"
                        f"Phone: {appointment.phone}\n"
                        f"Service: {appointment.service}\n"
                        f"Preferred date: {appointment.preferred_date} at {appointment.preferred_time}\n\n"
                        f"Message:\n{appointment.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.FIRM_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
                send_mail(
                    subject="We've received your appointment request - Munib and Co",
                    message=(
                        f"Dear {appointment.name},\n\n"
                        f"Thank you for booking an appointment with Munib and Co for {appointment.service}.\n"
                        f"We have received your request for {appointment.preferred_date} at {appointment.preferred_time} "
                        f"and will confirm shortly.\n\nRegards,\nMunib and Co"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appointment.email],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Your appointment request has been submitted. We'll confirm it shortly by email.")
            return redirect("appointments:book")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                "name": request.user.get_full_name(),
                "email": request.user.email,
                "phone": request.user.phone,
            }
        form = AppointmentForm(initial=initial)
    return render(request, "appointments/book_appointment.html", {"form": form})


@login_required
def my_appointments(request):
    appointments = request.user.appointments.all()
    return render(request, "appointments/my_appointments.html", {"appointments": appointments})


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)

    if request.method == "POST":
        form = AppointmentDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.appointment = appointment
            doc.uploaded_by = request.user
            doc.save()

            try:
                send_mail(
                    subject=f"New document uploaded - {appointment.service}",
                    message=(
                        f"{request.user.get_full_name() or request.user.username} uploaded a document "
                        f"(\"{doc.note or doc.filename}\") for their appointment on "
                        f"{appointment.preferred_date}. Log in to the staff dashboard to view it."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.FIRM_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Your document has been uploaded.")
            return redirect("appointments:detail", pk=appointment.pk)
    else:
        form = AppointmentDocumentForm()

    return render(request, "appointments/appointment_detail.html", {
        "appointment": appointment,
        "documents": appointment.documents.all(),
        "form": form,
    })


@login_required
def document_download(request, pk):
    document = get_object_or_404(AppointmentDocument, pk=pk)
    appointment = document.appointment

    is_owner = appointment.user_id == request.user.id
    if not (request.user.is_staff or is_owner):
        raise Http404("Document not found.")

    if not document.file.storage.exists(document.file.name):
        raise Http404("File no longer exists.")

    return FileResponse(
        document.file.open("rb"),
        as_attachment=True,
        filename=document.filename,
    )
