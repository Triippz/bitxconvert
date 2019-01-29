from django import template

from bitxconvert.convert.models import Conversion

register = template.Library()


@register.simple_tag
def get_user_conversions(user):
    conversions = Conversion.objects.filter(user=user)
    return conversions
