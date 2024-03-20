from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.views import LoginView as _LoginView
from .forms import LoginForm, UserRegistrationForm
from django.views.generic.edit import FormView


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


class RegistrationView(FormView):
    template_name = "registration/registration.html"
    # model = User
    form_class = UserRegistrationForm
    success_url = "social:login"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password2'])
        user.save()
        messages.success(self.request, "registration successful")
        return super().form_valid(form)
