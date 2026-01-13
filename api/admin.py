from django.contrib import admin
from unfold.admin import ModelAdmin
from api.models import User, UserConfirmation, Post, Media, Comment

@admin.register(User)
class UserAdmin(ModelAdmin):
	list_display = ["username", "first_name"]

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display_links = ("id", "user", "created_at")
    list_display = ("id", "user", "created_at")
    search_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display_links =  ("id", "user", "post", "created_at")
    list_display = ("id", "user", "post", "created_at")


@admin.register(Media)
class MediaAdmin(ModelAdmin):
    list_display_links  = ("id", "post")
    list_display = ("id", "post")

@admin.register(UserConfirmation)
class UserConfAdmin(ModelAdmin): 
	list_display = ["code", ] 