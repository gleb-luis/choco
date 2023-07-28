from django.contrib import admin
from django.contrib.sites.models import Site
from .models import SiteDetail, Advertisement, TopSetting, PageContent, ImageSetting


class SiteDetailInline(admin.StackedInline):
    """サイト詳細情報のインライン"""
    model = SiteDetail

class AdvertisementInline(admin.StackedInline):
    model = Advertisement

class TopSettingInline(admin.StackedInline):
    model = TopSetting

class PageContentInline(admin.StackedInline):
    model = PageContent

class ImageSettingInline(admin.StackedInline):
    model = ImageSetting

class SiteAdmin(admin.ModelAdmin):
    """Siteモデルを、管理画面でSiteDetailもインラインで表示できるように"""
    inlines = [SiteDetailInline, AdvertisementInline, TopSettingInline, PageContentInline, ImageSettingInline]


admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)