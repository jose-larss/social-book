from .models import Profile, Post, LikePost, FollowersCount

from django.contrib import admin

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)

