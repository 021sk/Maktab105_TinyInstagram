from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='', null=True, blank=True)
    job = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField('User', related_name='liked_posts', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)


class Image(models.Model):
    image_file = models.ImageField(upload_to='')
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250, null=True, blank=True,)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


