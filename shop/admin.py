from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Shop, Pref, LikeShop, ReviewShop, Tag


class ShopAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'content'# __all__ にするとうまく動かない
    list_display = ('id', 'name', 'pref', 'address', 'owner', 'hirata_flag', 'hirata_date', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('pref', 'owner')

admin.site.register(Shop, ShopAdmin)

@admin.register(Pref)
class PrefAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ReviewShop)
class ReviewShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'user', 'score', 'comment')


@admin.register(LikeShop)
class LikeShopAdmin(admin.ModelAdmin):
    list_display = ('liked_by', 'shop')