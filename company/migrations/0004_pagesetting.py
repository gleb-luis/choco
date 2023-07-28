# Generated by Django 2.2.1 on 2019-10-01 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20190817_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carousel1_title', models.CharField(max_length=36, verbose_name='トップページのカルーセル１タイトル')),
                ('carousel1_text', models.TextField(blank=True, verbose_name='トップページのカルーセル１テキスト')),
                ('carousel2_title', models.CharField(max_length=36, verbose_name='トップページのカルーセル２タイトル')),
                ('carousel2_text', models.TextField(blank=True, verbose_name='トップページのカルーセル２テキスト')),
                ('carousel3_title', models.CharField(max_length=36, verbose_name='トップページのカルーセル３タイトル')),
                ('carousel3_text', models.TextField(blank=True, verbose_name='トップページのカルーセル３テキスト')),
                ('about', models.TextField(blank=True, verbose_name='aboutページでこのサイトについての説明')),
                ('footer_text', models.TextField(blank=True, verbose_name='フッターに示すテキスト')),
            ],
        ),
    ]