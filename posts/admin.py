from django.contrib import admin

from .models import Post, Like, Country, Taste, Review

# Update for heroku (2022/12/28)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'views')
    list_editable = ('views', )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'liked_by',)
    list_display_links = ('post',)
    ordering = ('post',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country',)

@admin.register(Taste)
class TasteAdmin(admin.ModelAdmin):
    list_display = ('taste',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('post', 'score')