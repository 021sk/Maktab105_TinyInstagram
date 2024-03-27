from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.views import LoginView as _LoginView
from django.forms import Form
from django.views.decorators.http import require_POST

from .forms import LoginForm, UserRegistrationForm, EditUserForm, TicketForm, CreatePostForm, CommentForm
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Post, Image
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
    return render(request, 'social/list.html', {"posts": posts, "tag": tag, "form": CommentForm()})


# class PostCreateView(LoginRequiredMixin, View):
#     form_class = CreatePostForm
#
#     def get(self, request):
#         form = self.form_class()
#         return render(request, 'forms/create_post.html', {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             form.save_m2m()
#             Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
#             Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
#
#             return redirect('social:index')
#         return render(request, 'forms/create_post.html', {'form': form}
#                       )
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('social:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    context = {
        'post': post,
        'comments': comments
    }
    return render(request, "social/post_detail.html", context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.name = request.user.username
        comment.save()
    return redirect('social:posts_list')


@login_required()
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        post_likes_count = post.likes.count()
        response_data = {'likes_count': post_likes_count, 'liked': liked}
    else:
        response_data = {'error': 'post_id is required'}
    return JsonResponse(response_data)
