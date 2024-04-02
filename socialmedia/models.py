from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse, reverse_lazy



class User(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='account_images/', null=True, blank=True)
    job = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    following = models.ManyToManyField('self', through='Contact', symmetrical=False, related_name='followers')

    def get_absolute_url(self):
        return reverse('social:user_detail', args=[self.username])


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField('User', related_name='liked_posts', blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.first_name + ": " + self.description[:10] + '...'

    def get_absolute_url(self):
        return reverse_lazy('social:post_detail', args=[self.id])


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", verbose_name='post')
    image_file = models.ImageField(upload_to="post_images/")
    title = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250, null=True, blank=True, )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"{self.name}: {self.post}"
