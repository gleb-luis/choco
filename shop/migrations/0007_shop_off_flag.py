# Generated by Django 2.2.1 on 2019-10-24 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20191009_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='off_flag',
            field=models.BooleanField(default=False, verbose_name='表示しない'),
        ),
    ]
