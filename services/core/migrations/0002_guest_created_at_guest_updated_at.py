# Generated by Django 5.0.2 on 2024-02-13 03:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='guest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]