from django import forms
from .models import Appointment, AppointmentDocument


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["name", "email", "phone", "service", "preferred_date", "preferred_time", "message"]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control form-select" if name == "service" else existing + " form-control").strip()
            field.widget.attrs["class"] = "form-select" if name == "service" else "form-control"


class AppointmentDocumentForm(forms.ModelForm):
    class Meta:
        model = AppointmentDocument
        fields = ["file", "note"]
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "note": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "What is this file? e.g. \"CNIC copy\", \"Completed tax return\"",
            }),
        }

    def clean_file(self):
        file = self.cleaned_data["file"]
        max_size_mb = 10
        if file.size > max_size_mb * 1024 * 1024:
            raise forms.ValidationError(f"File is too large. Maximum size is {max_size_mb}MB.")
        allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx", ".xls", ".xlsx"]
        ext = "." + file.name.rsplit(".", 1)[-1].lower() if "." in file.name else ""
        if ext not in allowed_extensions:
            raise forms.ValidationError(
                "Unsupported file type. Allowed: PDF, JPG, PNG, DOC/DOCX, XLS/XLSX."
            )
        return file
