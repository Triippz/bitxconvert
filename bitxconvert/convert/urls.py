from django.urls import path

from bitxconvert.convert.views import home_view, upload_view, upload_success, download

app_name = "convert"
urlpatterns = [
    path("", view=home_view, name="home"),
    path("upload/", view=upload_view, name="upload"),
    path("upload/success/", view=upload_success, name="success"),
    path("download/(<file>\d+)/", view=download, name="download")
]
