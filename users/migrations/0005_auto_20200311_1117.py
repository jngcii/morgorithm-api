# Generated by Django 3.0.3 on 2020-03-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_group_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirm_code',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
