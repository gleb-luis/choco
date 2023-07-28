from django.db import models
from django.contrib.sites.models import Site

class SiteDetail(models.Model):
    """Siteと1対1で紐づくサイト詳細情報"""
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=255, default='Webサイトのタイトル')
    description = models.TextField('サイトの説明', max_length=255, default='Webサイトの説明')
    keywords = models.CharField('サイトのSEOキーワード', max_length=255, default='Webサイトのキーワード')
    author = models.CharField('管理者', max_length=255, default='CHOCO.FAN管理者')
    email = models.EmailField('管理者アドレス', max_length=255, default='your_mail@gmail.com')
    homepage_url = models.URLField('公式サイト', blank=True)
    insta_url = models.URLField('Instagram URL', blank=True)
    twitter = models.URLField('Twitter URL', blank=True)
    facebook = models.URLField('FaceBook URL', blank=True)

    def __str__(self):
        return self.author


class Advertisement(models.Model):
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    google_ad_side1 = models.TextField('アドセンスHTML サイドバー用1', blank=True)
    google_ad_side2 = models.TextField('アドセンスHTML サイドバー用2', blank=True)
    google_ad_main1 = models.TextField('アドセンスHTML メイン（col-9）用1', blank=True)
    google_ad_main2 = models.TextField('アドセンスHTML メイン（col-9）用2', blank=True)
    rakuten_ad_side1 = models.TextField('楽天アフィリエイト サイドバー用1', blank=True)
    rakuten_ad_side2 = models.TextField('楽天アフィリエイト サイドバー用2', blank=True)
    a8_ad_side1 = models.TextField('A8ネット サイドバー用1', blank=True)
    a8_ad_side2 = models.TextField('A8ネット サイドバー用2', blank=True)
    amazon_ad_side1 = models.TextField('Amazon サイドバー用1', blank=True)
    amazon_ad_side2 = models.TextField('Amazon サイドバー用2', blank=True)

    def __int__(self):
        return self.site


class TopSetting(models.Model):
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    carousel1_title = models.CharField('トップページのカルーセル１タイトル', max_length=36, blank=False)
    carousel1_text = models.TextField('トップページのカルーセル１テキスト', blank=True)
    carousel2_title = models.CharField('トップページのカルーセル２タイトル', max_length=36, blank=False)
    carousel2_text = models.TextField('トップページのカルーセル２テキスト', blank=True)
    carousel3_title = models.CharField('トップページのカルーセル３タイトル', max_length=36, blank=False)
    carousel3_text = models.TextField('トップページのカルーセル３テキスト', blank=True)

    def __str__(self):
        return self.carousel1_title


class PageContent(models.Model):
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    about = models.TextField('aboutページでこのサイトについての説明', blank=True)

    def __int__(self):
        return self.site


class ImageSetting(models.Model):
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    shop_default_thumbnail = models.ImageField('店舗サムネイルがない場合の代替画像', upload_to="image/site/", blank=True, null=True)
    shop_default_thumbnail2 = models.ImageField('店舗サムネイルがない場合の代替画像', upload_to="image/site/", blank=True, null=True)
    shop_default_thumbnail3 = models.ImageField('店舗サムネイルがない場合の代替画像', upload_to="image/site/", blank=True, null=True)
    column_default_thumbnail = models.ImageField('コラムサムネイルがない場合の代替画像', upload_to="image/site/", blank=True, null=True)

    def __int__(self):
        return self.site