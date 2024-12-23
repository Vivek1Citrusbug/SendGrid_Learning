import sendgrid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from sendgrid import SendGridAPIClient
from django.conf import settings
from sendgrid.helpers.mail import *
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class RegistrationView(FormView):
    """This view is used for registering new user"""

    template_name = "accounts/registration.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("user-login")

    # def form_valid(self, form):
    #     form.save()

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        print("after usre save")
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv("EMAIL_HOST_PASSWORD"))
        from_email = Email("vivek1.citrusbug@gmail.com")
        subject = "Welcome to Our Platform!"
        content = Content("text/plain", "<strong>It is easy to send mail with Python and SendGrid</strong>")
        message = Mail(
            from_email=from_email,
            to_emails=user.email,  
            subject=subject,
            html_content=content
        )
        try:
            sg = SendGridAPIClient(api_key=os.getenv("EMAIL_HOST_PASSWORD"))
            response = sg.send(message)
            print(f"Email sent successfully, status code: {response.status_code}")
            messages.success(self.request, "Registration successful! Please check your email for confirmation.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        return super().form_valid(form)

class CustomLoginView(LoginView):
    """This view is used for login Existing user"""

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("blog_list")


def logout_view(request):
    """This view is used for logging out user"""

    logout(request)
    return redirect("home_page")


@login_required(login_url="user-login")
def user_profile(request):
    """This view is used for redirecting user to profile page"""

    return render(request, "accounts/profile.html")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """This view is used for listing profile details"""

    model = UserProfile
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """This view is used for profile update"""

    model = UserProfile
    form_class = UserProfileForm
    template_name = "accounts/edit_profile.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
