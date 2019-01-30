from django.db import models
from django import forms

# Create your models here.
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, InlinePanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.blocks import RawHTMLBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from bitxconvert.utils.models import ContactFields


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', null=True, blank=True)
    instagram = models.URLField(
        max_length=255, help_text='Your Instagram URL', null=True, blank=True)
    twitter = models.URLField(
        max_length=255, help_text='Your Twitter URL', null=True, blank=True)
    youtube = models.URLField(
        help_text='Your YouTube Channel URL', null=True, blank=True)
    linkedin = models.URLField(
        max_length=255, help_text='Your Linkedin URL', null=True, blank=True)
    github = models.URLField(
        max_length=255, help_text='Your Github URL', null=True, blank=True)
    facebook_appid = models.CharField(
        max_length=255, help_text='Your Facbook AppID', null=True, blank=True)
    google_analytics_key = models.CharField(
        max_length=255, help_text='Your Google Analytics Key', null=True, blank=True)


class CoreIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        newspages = self.get_children().live().order_by('-first_published_at')
        context['corepages'] = newspages
        return context


class AboutPage(Page):
    date = models.DateField("Post date")
    revised_date = models.DateField("revised date", blank=True)
    intro = models.CharField(max_length=250)
    intro_title = RichTextField(blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('intro_title'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('revised_date')
        ], heading="About Information"),
        FieldPanel('intro'),
        FieldPanel('intro_title'),
        FieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


class Terms(Page):
    date = models.DateField("Post date")
    revised_date = models.DateField("revised date", blank=True)
    intro = models.CharField(max_length=250)
    intro_title = RichTextField(blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('intro_title'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('revised_date')
        ], heading="Terms of Service Information"),
        FieldPanel('intro'),
        FieldPanel('intro_title'),
        FieldPanel('body'),
    ]
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


class PrivacyPolicy(Page):
    date = models.DateField("Post date", blank=False)
    revised_date = models.DateField("revised date", blank=True)
    intro = models.CharField(max_length=250)
    intro_title = RichTextField(blank=True)
    body = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('intro_title'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('revised_date')
        ], heading="Privacy Policy Information"),
        FieldPanel('intro'),
        FieldPanel('intro_title'),
        FieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='custom_form_fields')


class FormPage(AbstractEmailForm):
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        InlinePanel('custom_form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

    def get_form_fields(self):
        return self.custom_form_fields.all()


@register_snippet
class ExternalFooterLinks(models.Model):
    url = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('url'),
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name


class DonatePage(Page):
    intro_title = models.CharField(max_length=250)
    intro = RichTextField(blank=False)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('intro_title'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('intro_title'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]
