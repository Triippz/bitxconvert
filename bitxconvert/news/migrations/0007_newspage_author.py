# Generated by Django 2.0.10 on 2019-01-23 14:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20190123_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspage',
            name='author',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]