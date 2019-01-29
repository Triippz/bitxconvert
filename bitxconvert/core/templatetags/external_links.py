from django import template
from bitxconvert.core.models import ExternalFooterLinks

register = template.Library()


# Advert snippets
@register.inclusion_tag('core/includes/external_footer_links.html', takes_context=True)
def external_links(context):
    return {
        'links': ExternalFooterLinks.objects.all(),
        'request': context['request'],
    }
