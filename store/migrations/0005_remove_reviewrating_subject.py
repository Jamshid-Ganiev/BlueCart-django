# Generated by Django 4.1.7 on 2023-04-12 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_reiviewrating_reviewrating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='subject',
        ),
    ]
