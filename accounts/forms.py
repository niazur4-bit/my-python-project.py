from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm,
)
from .models import User


class ClientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    company_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "email",
            "phone", "company_name", "password1", "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        user.company_name = self.cleaned_data.get("company_name", "")
        if commit:
            user.save()
        return user


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Username"})
        self.fields["password"].widget.attrs.update({"class": "form-control", "placeholder": "Password"})


class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "you@example.com"})


class StyledSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({"class": "form-control", "placeholder": "New password"})
        self.fields["new_password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm new password"})


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "address", "cnic", "company_name", "profile_photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "profile_photo":
                field.widget.attrs.update({"class": "form-control"})
