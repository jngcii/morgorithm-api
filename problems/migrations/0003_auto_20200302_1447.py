# Generated by Django 3.0.3 on 2020-03-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20200302_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='is_solved',
            field=models.BooleanField(default=False),
        ),
    ]
