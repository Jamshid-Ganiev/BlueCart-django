# Generated by Django 4.1.7 on 2023-04-12 17:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0003_reiviewrating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReiviewRating',
            new_name='ReviewRating',
        ),
    ]