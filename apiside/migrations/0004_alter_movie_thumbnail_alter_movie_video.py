# Generated by Django 5.0.6 on 2024-10-17 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiside', '0003_plan_rating_table_usersubscriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='thumbnail',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='video',
            field=models.CharField(max_length=200),
        ),
    ]
