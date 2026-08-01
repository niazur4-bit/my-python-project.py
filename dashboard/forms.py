from django import forms

from appointments.models import Appointment


class AppointmentReplyForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["admin_reply", "status"]
        widgets = {
            "admin_reply": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write a reply the client will see on their account (e.g. confirming a time, "
                               "asking for a document, or answering their question)...",
            }),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "admin_reply": "Reply to client",
            "status": "Update appointment status",
        }
