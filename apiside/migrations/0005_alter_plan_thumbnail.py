# Generated by Django 5.0.6 on 2024-10-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiside', '0004_alter_movie_thumbnail_alter_movie_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='thumbnail',
            field=models.CharField(max_length=200),
        ),
    ]
