from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import ContactForm


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                send_mail(
                    subject=f"New website inquiry: {contact_message.subject}",
                    message=(
                        f"Name: {contact_message.name}\n"
                        f"Email: {contact_message.email}\n"
                        f"Phone: {contact_message.phone}\n\n"
                        f"Message:\n{contact_message.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.FIRM_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Thank you for reaching out. We'll get back to you within 1 business day.")
            return redirect("contact:contact")
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {
        "form": form,
        "maps_src": settings.GOOGLE_MAPS_EMBED_SRC,
    })
