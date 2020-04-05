# Generated by Django 3.0.5 on 2020-04-05 13:38

import config.file_util
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to=config.file_util.user_directory_path),
        ),
    ]
