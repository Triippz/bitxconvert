from itertools import chain

from django import template

from bitxconvert.core.models import CoreIndexPage, AboutPage, Terms, PrivacyPolicy, FormPage

register = template.Library()


@register.simple_tag
def get_core_pages():
    about_pages = AboutPage.objects.live()
    terms_pages = Terms.objects.live()
    privacy_pages = PrivacyPolicy.objects.live()
    form_pages = FormPage.objects.live()
    pages = list(chain(about_pages, terms_pages, privacy_pages, form_pages))
    return pages
