# Generated by Django 3.0.5 on 2020-05-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20200506_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='to',
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('like', 'like'), ('comment', 'comment')], max_length=20),
        ),
    ]