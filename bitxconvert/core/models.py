from django.db import models
from django import forms

# Create your models here.
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.search import index


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
