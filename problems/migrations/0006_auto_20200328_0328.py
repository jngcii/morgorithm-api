# Generated by Django 3.0.3 on 2020-03-28 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20200328_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='originprob',
            name='category',
            field=models.CharField(blank=True, choices=[('Programmers', 'programmers'), ('BaekJoon', 'baekjoon'), ('SWEA', 'swea')], max_length=255, null=True),
        ),
    ]
