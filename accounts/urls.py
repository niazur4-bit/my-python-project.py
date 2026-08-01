from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .forms import StyledPasswordResetForm, StyledSetPasswordForm

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.ClientLoginView.as_view(), name="login"),
    path("logout/", views.ClientLogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
    path("dashboard/client/", views.client_dashboard, name="client_dashboard"),
    path("profile/", views.profile, name="profile"),

    # Forgot-password flow (Django's built-in views, custom templates below)
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            form_class=StyledPasswordResetForm,
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            form_class=StyledSetPasswordForm,
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
