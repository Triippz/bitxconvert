from django import forms
from django.conf import settings


class ConvertFilesForm(forms.Form):
    exchange = forms.ChoiceField(
        choices=settings.CONVERT_SUPPORTED_EXCHANGES,
        widget=forms.Select)
    service = forms.ChoiceField(
        choices=settings.CONVERT_SUPPORTED_SERVICES,
        widget=forms.Select)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

