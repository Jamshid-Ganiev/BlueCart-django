# Generated by Django 4.1.7 on 2023-04-25 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='userProfile/default_profile_pic.png', upload_to='userProfile/'),
        ),
    ]