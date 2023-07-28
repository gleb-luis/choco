from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Column


class ColumnAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = 'content'# __all__ にするとうまく動かない
    list_display = ('created_at', 'updated_at', 'author', 'title', 'is_draft')
    list_display_links = ('title',)
    
admin.site.register(Column, ColumnAdmin)
