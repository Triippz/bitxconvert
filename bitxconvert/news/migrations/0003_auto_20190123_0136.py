# Generated by Django 2.0.10 on 2019-01-23 01:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('news', '0002_newspage'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='newspage',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='newspage',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Post date'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newspage',
            name='intro',
            field=models.CharField(max_length=250),
        ),
    ]
