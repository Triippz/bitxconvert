from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, MultiFieldPanel
from wagtail.core.models import Orderable


class ContactFields(models.Model):
    name_organization = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    telephone_2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    email_2 = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('name_organization',
                   'The full/formatted name of the person or organisation'),
        FieldPanel('telephone'),
        FieldPanel('telephone_2'),
        FieldPanel('email'),
        FieldPanel('email_2'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


