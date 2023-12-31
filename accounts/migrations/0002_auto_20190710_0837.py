# Generated by Django 2.2 on 2019-07-09 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fb',
            field=models.URLField(blank=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='user',
            name='insta',
            field=models.URLField(blank=True, verbose_name='Instagram'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_bloger',
            field=models.BooleanField(default=False, verbose_name='ブログ執筆可'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.BooleanField(default=False, verbose_name='ショップオーナー'),
        ),
        migrations.AddField(
            model_name='user',
            name='tw',
            field=models.URLField(blank=True, verbose_name='Twitter'),
        ),
    ]
