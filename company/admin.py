from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import News, PrivacyPolicy, TermsOfUse, PageSetting


class NewsAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'

admin.site.register(News, NewsAdmin)


class TermsOfUseAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'text'

admin.site.register(TermsOfUse, TermsOfUseAdmin)

class PrivacyPolicyAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'text'

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)


@admin.register(PageSetting)
class PageSettingAdmin(admin.ModelAdmin):
    list_display = ('carousel1_title', 'carousel2_title', 'carousel3_title')

 