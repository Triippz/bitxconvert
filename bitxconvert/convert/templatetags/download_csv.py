from django import template

from django.conf import settings

from django.core.files.storage import default_storage


register = template.Library()


@register.simple_tag
def download_csv(file_name):
    if default_storage.exists('media/csv/{}'.format(file_name)):
        return {
            'error': False,
            'message': "{}{}{}".format(settings.MEDIA_URL, settings.DOWNLOAD_FILE_DIR, file_name)
        }
    else:
        return {
                'error': True,
                'message': "We can't seem to find that file. If you just converted a file, "
                           "please check back in a minute"
            }

