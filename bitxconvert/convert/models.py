from django.db import models
from django.conf import settings
from django.utils import timezone

from config.settings.production import MediaRootS3Boto3Storage


class Conversion(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    number_of_files = models.IntegerField(blank=True, default=0)
    exchange = models.CharField(max_length=50, blank=False, choices=settings.CONVERT_SUPPORTED_EXCHANGES)
    tax_service = models.CharField(max_length=100, blank=False, choices=settings.CONVERT_SUPPORTED_SERVICES)
    trades_processed = models.IntegerField(blank=False, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255, blank=False)
    file = models.FileField(blank=True, storage=MediaRootS3Boto3Storage())

    def get_file_url(self):
        return self.file.url
