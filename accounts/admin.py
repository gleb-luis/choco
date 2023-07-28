from django.contrib import admin

from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'follower_count')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('followee', 'follower')
