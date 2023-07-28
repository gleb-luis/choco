# Generated by Django 2.2.1 on 2019-11-08 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('sitesetting', '0002_auto_20191029_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_default_thumbnail', models.ImageField(blank=True, null=True, upload_to='image/site/', verbose_name='店舗サムネイルがない場合の代替画像')),
                ('shop_default_thumbnail2', models.ImageField(blank=True, null=True, upload_to='image/site/', verbose_name='店舗サムネイルがない場合の代替画像')),
                ('shop_default_thumbnail3', models.ImageField(blank=True, null=True, upload_to='image/site/', verbose_name='店舗サムネイルがない場合の代替画像')),
                ('column_default_thumbnail', models.ImageField(blank=True, null=True, upload_to='image/site/', verbose_name='コラムサムネイルがない場合の代替画像')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='sites.Site', verbose_name='Site')),
            ],
        ),
    ]
