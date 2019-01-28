from django.contrib import admin

# Register your models here.
from bitxconvert.core.models import AboutPage, Terms, PrivacyPolicy

admin.site.register(AboutPage)
admin.site.register(Terms)
admin.site.register(PrivacyPolicy)
