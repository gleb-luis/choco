from django.db import models

class CompanyInfo(models.Model):
    official_fb = models.URLField('オフィシャルFBページ', blank=True)
    official_tw = models.URLField('オフィシャルTW', blank=True)
    official_insta = models.URLField('オフィシャルInstagram', blank=True)
    official_site = models.URLField('オフィシャルサイト', blank=True)


class PrivacyPolicy(models.Model):
    text = models.TextField(blank=True)
    version = models.CharField(max_length=5, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.version)
    
class TermsOfUse(models.Model):
    text = models.TextField(blank=True)
    version = models.CharField(max_length=5, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.version)

# 会社からのユーザーへのお知らせを告知するためのテーブル
class News(models.Model):
    title = models.CharField(max_length=120, blank=False)
    text = models.TextField(blank=True)
    public_date = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class PageSetting(models.Model):
    carousel1_title = models.CharField('トップページのカルーセル１タイトル', max_length=36, blank=False)
    carousel1_text = models.TextField('トップページのカルーセル１テキスト', blank=True)
    carousel2_title = models.CharField('トップページのカルーセル２タイトル', max_length=36, blank=False)
    carousel2_text = models.TextField('トップページのカルーセル２テキスト', blank=True)
    carousel3_title = models.CharField('トップページのカルーセル３タイトル', max_length=36, blank=False)
    carousel3_text = models.TextField('トップページのカルーセル３テキスト', blank=True)
    about = models.TextField('aboutページでこのサイトについての説明', blank=True)

    def __str__(self):
        return str(self.carousel1_title)
