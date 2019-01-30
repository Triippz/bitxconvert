# Create your views here.
from django.template.response import TemplateResponse


def light_box_view(request):
    return TemplateResponse( request, "core/mdb-addons/mdb-lightbox-ui.html")
