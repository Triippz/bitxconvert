# Generated by Django 2.0.10 on 2019-01-28 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20190128_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmediasettings',
            name='google_analytics_key',
            field=models.CharField(blank=True, help_text='Your Google Analytics Key', max_length=255, null=True),
        ),
    ]
