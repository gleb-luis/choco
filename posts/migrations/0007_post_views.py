# Generated by Django 2.2.1 on 2019-07-24 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='アクセス数'),
        ),
    ]
