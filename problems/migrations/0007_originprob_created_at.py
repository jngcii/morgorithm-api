# Generated by Django 3.0.5 on 2020-05-29 10:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_auto_20200328_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='originprob',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]