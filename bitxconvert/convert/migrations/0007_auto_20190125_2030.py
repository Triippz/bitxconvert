# Generated by Django 2.0.10 on 2019-01-25 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0006_auto_20190125_2028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversion',
            old_name='date',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='conversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
