from django import template
from django.conf import settings
register = template.Library()


@register.simple_tag
def get_ga_key():
    return getattr(settings, 'GOOGLE_ANALYTICS_KEY', "")

