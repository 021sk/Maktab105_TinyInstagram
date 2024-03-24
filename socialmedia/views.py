from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.views import LoginView as _LoginView
from django.forms import Form
from .forms import LoginForm, UserRegistrationForm, EditUserForm, TicketForm
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Post
from taggit.models import Tag
from django.core.mail import send_mail


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

    # class EditUserView(UpdateView, SuccessMessageMixin,LoginRequiredMixin):
    #     model = User
    #     fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'bio', 'photo',
    #               'job']
    #


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated")
            return redirect("social:index")
    else:
        user_form = EditUserForm(instance=request.user)
    return render(request, 'registration/edit_account.html', {"forms": user_form})


def ticket(request):
    sent = False
    if request.method == "POST":

        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(subject=cd['subject'], message=message, from_email='shahaabkabiri73@gmail.com',
                      recipient_list=['amkabiri64@gmail.com'], fail_silently=True)
            sent = True

    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {'forms': form, 'sent': sent})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'social/list.html', {"posts": posts, "tag": tag})
