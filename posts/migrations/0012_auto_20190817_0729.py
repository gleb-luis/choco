# Generated by Django 2.2.1 on 2019-08-16 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20190803_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='average_score',
        ),
        migrations.RemoveField(
            model_name='post',
            name='review_count',
        ),
        migrations.AlterField(
            model_name='review',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
    ]
