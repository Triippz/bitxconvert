import os

from django.http import HttpResponse, Http404, FileResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.conf import settings
from django.urls import reverse

from bitxconvert.convert.forms import ConvertFilesForm
from bitxconvert.convert.utils.parse_file import parse_files
from bitxconvert.convert.utils.validation import validate_convert


def home_view(request):
    if request.method == 'POST':
        is_valid = validate_convert(request.POST, request.FILES)
        if is_valid[0]:
            exchange = request.POST['exchange']
            service = request.POST['convert']
            files = request.FILES.getlist('file_field')
            file_info = parse_files(exchange, service, files, request.user)

            ctx = {
                "processed": file_info['conversion'].trades_processed,
                "exchange": file_info['conversion'].exchange,
                "service": file_info['conversion'].tax_service,
                "files": file_info['conversion'].number_of_files,
                "created_at": str(file_info['conversion'].created_at),
                "file_name": file_info['results']['file_name'],
                "conversion_id": file_info['conversion'].id
            }
            # return TemplateResponse (
            #     request, template="convert/success.html", context=ctx
            # )
            request.session['download_ctx'] = ctx
            return HttpResponseRedirect(reverse('convert:success'))

        form = ConvertFilesForm()
        return TemplateResponse(
            request, "convert/home.html", {'form': form, 'error': is_valid[1]}
        )

    form = ConvertFilesForm()
    return TemplateResponse(
        request, "convert/home.html", {'form': form}
    )


def download(request, file):
    file_path = os.path.join(settings.MEDIA_ROOT, settings.DOWNLOAD_FILE_DIR, file)
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = FileResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def upload_view(request):
    return


def upload_success(request):
    return TemplateResponse(
        request, template="convert/success.html", context=request.session['download_ctx']
    )


def upload(request):
    return
