from django.db import models
from accounts.models import User
from django.db.models import Avg


class Shop(models.Model):
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField("店舗名", max_length=100, blank=False, unique=True)
    thumbnail = models.ImageField(upload_to="image/shop/", blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to="image/shop/", blank=True, null=True)
    thumbnail3 = models.ImageField(upload_to="image/shop/", blank=True, null=True)
    short_content = models.CharField("店舗概要", max_length=100, blank=False)
    content = models.TextField("店舗紹介文", blank=False)
    shop_url = models.URLField("店舗URL", blank=True)
    shop_fb = models.URLField('Facebook（店舗アカウント）', blank=True)
    shop_tw = models.URLField('Twitter（店舗アカウント）', blank=True)
    shop_insta = models.URLField('Instagram（店舗アカウント）', blank=True)
    shop_line = models.CharField("Line公式", max_length=100, blank=True)
    shop_tel = models.CharField("店舗電話番号", blank=True, max_length=12)
    shop_email = models.EmailField("店舗メール", blank=True)
    zipcode = models.CharField("店舗郵便番号", max_length=8)
    pref = models.ForeignKey('Pref', on_delete=models.PROTECT)
    tag = models.ManyToManyField('Tag', blank=True)
    address = models.CharField("店舗住所", max_length=200, help_text="都道府県を含まない住所")
    hirata_flag = models.BooleanField("hirada103導入かどうか", default=False)
    hirata_date = models.DateField("Hirata103導入日", blank=True, default='2001-01-01')
    views = models.PositiveIntegerField('アクセス数', default=0)
    off_flag = models.BooleanField('表示しない', default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def get_review_count(self):
        review_count = ReviewShop.objects.filter(shop=self).count()
        return review_count

    def get_average_score(self):
        average_score = ReviewShop.objects.filter(shop=self).aggregate(Avg('score'))
        return average_score['score__avg']

    def get_percent(self):
        percent = round(self.average_score / 5 * 100)
        return percent

    def get_like_count(self):
        like_count = LikeShop.objects.filter(shop=self).count()
        return like_count

class LikeShop(models.Model):
    liked_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)


class Pref(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=4)
    
    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=32)
    
    def __str__(self):
        return str(self.name)

    def get_latest_shop(self):
        result = Shop.objects.filter(tag=self).order_by('-created_at')[:5]
        return result


SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]

class ReviewShop(models.Model):
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    comment = models.TextField(verbose_name='レビューコメント', blank=False)
    score = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('shop', 'user')

    def __str__(self):
        return str(self.shop)

    def get_percent(self):
        percent = round(self.score / 5 * 100)
        return percent