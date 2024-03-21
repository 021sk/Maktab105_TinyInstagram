from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.views import LoginView as _LoginView
from django.forms import Form
from .forms import LoginForm, UserRegistrationForm
from django.views.generic.edit import FormView, CreateView
from django.contrib.messages.views import SuccessMessageMixin


def log_out(request):
    logout(request)
    messages.info(request, 'You have successfully logged out!')
    return HttpResponse('you are logged out!')


class LoginView(_LoginView):
    redirect_authenticated_user = True
    next_page = "social:index"
    template_name = "registration/login.html"
    authentication_form = LoginForm

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, "Welcome 😉")
        return result


def index(request):
    return HttpResponse("you are login")


class RegistrationView(CreateView, SuccessMessageMixin):
    template_name = "registration/registration.html"
    # model = User
    form_class = UserRegistrationForm
    success_message = "Your profile was created successfully"
    success_url = reverse_lazy("social:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "Registration Successful")

        return super().form_valid(form)
