# Generated by Django 2.2.1 on 2019-08-02 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('column', '0003_auto_20190722_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='アクセス数'),
        ),
        migrations.AlterField(
            model_name='column',
            name='content',
            field=models.TextField(verbose_name='コンテンツ'),
        ),
    ]
