from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from appointments.models import Appointment
from .forms import ClientRegistrationForm, StyledAuthenticationForm, ProfileUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard_redirect")

    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.get_full_name() or user.username}! Your account has been created.")
            return redirect("accounts:dashboard_redirect")
    else:
        form = ClientRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


class ClientLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse("accounts:dashboard_redirect")


class ClientLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect("dashboard:index")
    return redirect("accounts:client_dashboard")


@login_required
def client_dashboard(request):
    appointments = Appointment.objects.filter(user=request.user).order_by("-preferred_date")[:10]
    context = {
        "appointments": appointments,
        "appointment_count": Appointment.objects.filter(user=request.user).count(),
        "pending_count": Appointment.objects.filter(user=request.user, status="pending").count(),
    }
    return render(request, "accounts/client_dashboard.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})
