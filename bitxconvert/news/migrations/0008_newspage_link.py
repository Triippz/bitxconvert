# Generated by Django 2.0.10 on 2019-01-23 14:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_newspage_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspage',
            name='link',
            field=models.URLField(blank=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
