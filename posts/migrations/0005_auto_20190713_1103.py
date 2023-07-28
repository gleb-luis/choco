# Generated by Django 2.2.1 on 2019-07-13 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_country_taste'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='posts.Country'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='taste',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='posts.Taste'),
            preserve_default=False,
        ),
    ]