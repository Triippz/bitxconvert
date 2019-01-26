from django.db import models
from django.conf import settings
from django.utils import timezone


class Conversion(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    number_of_files = models.IntegerField(blank=True, default=0)
    exchange = models.CharField(max_length=50, blank=False, choices=settings.CONVERT_SUPPORTED_EXCHANGES)
    tax_service = models.CharField(max_length=100, blank=False, choices=settings.CONVERT_SUPPORTED_SERVICES)
    trades_processed = models.IntegerField(blank=False, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
