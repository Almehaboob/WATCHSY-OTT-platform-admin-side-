# Generated by Django 5.0.6 on 2024-10-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiside', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
                ('video', models.FileField(upload_to='videos/')),
                ('description', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
            ],
        ),
    ]
