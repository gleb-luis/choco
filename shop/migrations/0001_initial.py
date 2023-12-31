# Generated by Django 2.2.1 on 2019-09-25 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pref',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='店舗名')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='image/shop/')),
                ('thumbnail2', models.ImageField(blank=True, null=True, upload_to='image/shop/')),
                ('thumbnail3', models.ImageField(blank=True, null=True, upload_to='image/shop/')),
                ('content', models.TextField(verbose_name='店舗紹介文')),
                ('url', models.URLField(blank=True, null=True, verbose_name='店舗URL')),
                ('zipcode', models.CharField(max_length=8, verbose_name='店舗郵便番号')),
                ('address', models.CharField(help_text='都道府県を含まない住所', max_length=200, verbose_name='店舗住所')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='アクセス数')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pref', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.Pref')),
            ],
        ),
    ]
