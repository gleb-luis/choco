from django.db import models
from accounts.models import User
from shop.models import Shop


# Create your models here.
class Column(models.Model):
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=100, blank=False)
    is_index = models.BooleanField("目次有無", default=True, help_text="H2タグが自動的に目次として認識されます")
    is_draft = models.BooleanField("下書きの場合はチェック", default=False, help_text="下書きの場合はチェックを入れてください。公開されません。")
    thumbnail = models.ImageField(upload_to="image/column/", blank=True, null=True)
    content = models.TextField("コンテンツ")
    content_script = models.TextField("スクリプト", blank=True)
    views = models.PositiveIntegerField('アクセス数（累積）', default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    
    def get_author_shop(self):
        name = Shop.objects.filter(owner=self.author).first()
        return name