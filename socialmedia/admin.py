from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class ImageInline(admin.StackedInline):
    model = Image


class CommentInline(admin.StackedInline):
    model = Comment


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone_number')}),

    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'description']
    ordering = ['created']
    search_fields = ['description']
    inlines = [ImageInline, CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'active']
    list_filter = ['active', 'created','updated',]
    search_fields = ['name', 'body']
    list_editable = ['active']

