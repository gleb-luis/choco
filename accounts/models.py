from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# AbstractUser: Djangoが用意しているUserモデルを継承する
class User(AbstractUser):
    # アイコンを画像を保存できるImageFieldとして定義する
    icon = models.ImageField(upload_to="image/accounts/", blank=True, null=True)
    profile = models.TextField('プロフィール', blank=True)
    nickname = models.CharField('ニックネーム', max_length=20, blank=True)
    fb = models.URLField('Facebook', blank=True)
    tw = models.URLField('Twitter', blank=True)
    insta = models.URLField('Instagram', blank=True)
    follower_count = models.PositiveIntegerField('フォローワーの数', default=0)
    is_columnist = models.BooleanField('コラム執筆可', default=False)
    is_owner = models.BooleanField('ショップオーナー', default=False)

    # 作成を成功したら'chocobar:profile'と定義されているURLに飛ぶ
    def get_absolute_url(self):
        return reverse(
            'chocobar:profile', kwargs={'username': self.username})

    # フォロー中のユーザーを取得
    def get_following_user(self):
        following = Follow.objects.filter(follower = self)
        return following

    
class Follow(models.Model):
    followee = models.IntegerField('フォローされているUserのID', default=0)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    followed_at = models.DateField(auto_now_add=True)

    def __int__(self):
        return self.followee