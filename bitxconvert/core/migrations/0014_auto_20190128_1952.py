# Generated by Django 2.0.10 on 2019-01-28 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20190128_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalfooterlinks',
            name='link_name',
        ),
        migrations.RemoveField(
            model_name='externalfooterlinks',
            name='link_url',
        ),
    ]
