import inspect
import os
import datetime

from django.http import Http404, FileResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.conf import settings
from django.urls import reverse

from bitxconvert.convert.forms import ConvertFilesForm
from bitxconvert.convert.utils.parse_file import parse_files
from bitxconvert.convert.utils.validation import validate_convert
from bitxconvert.utils.exceptions import IncorrectFileFormat, IncorrectExchangeException, EmptyExchangeField, \
    EmptyServiceField, UploadFileError


def home_view(request):
    if request.method == 'POST':
        try:
            validate_convert(request.POST, request.FILES)

            exchange = request.POST['exchange']
            service = request.POST['convert']
            files = request.FILES.getlist('file_field')
            try:
                file_info = parse_files(exchange, service, files, request.user)
            except IncorrectFileFormat as e:
                print("ERROR: {} : {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
                form = ConvertFilesForm()
                return TemplateResponse(
                    request, "convert/home.html", {'form': form, 'error': e}
                )
            except IncorrectExchangeException as e:
                print("ERROR: {} : {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
                form = ConvertFilesForm()
                return TemplateResponse(
                    request, "convert/home.html", {'form': form, 'error': e}
                )
            except UploadFileError as e:
                print("ERROR: {} : {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
                form = ConvertFilesForm()
                return TemplateResponse(
                    request, "convert/home.html", {'form': form, 'error': e}
                )
            except Exception as e:
                print("ERROR: {} : {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
                form = ConvertFilesForm()
                return TemplateResponse(
                    request, "convert/home.html", {'form': form, 'error': "Error uploading file. Please try again "
                                                                          "later. If the problem persists, please "
                                                                          "contact us."}
                )

            if settings.DEBUG:
                ctx = {
                    "processed": file_info['conversion'].trades_processed,
                    "exchange": file_info['conversion'].exchange,
                    "service": file_info['conversion'].tax_service,
                    "files": file_info['conversion'].number_of_files,
                    "created_at": str(file_info['conversion'].created_at),
                    "file_name": file_info['results']['file_name'],
                    "conversion_id": file_info['conversion'].id,
                    "debug": settings.DEBUG
                }
            else:
                ctx = {
                    "processed": file_info['conversion'].trades_processed,
                    "exchange": file_info['conversion'].exchange,
                    "service": file_info['conversion'].tax_service,
                    "files": file_info['conversion'].number_of_files,
                    "created_at": str(file_info['conversion'].created_at),
                    "file_name": file_info['results']['file_name'],
                    "conversion_id": file_info['conversion'].id,
                    "debug": settings.DEBUG,
                    "file_url": file_info['conversion'].file_url
                }
            request.session['download_ctx'] = ctx
            return HttpResponseRedirect(reverse('convert:success'))
        except EmptyExchangeField as e:
            form = ConvertFilesForm()
            return TemplateResponse(
                request, "convert/home.html", {'form': form, 'error': e}
            )
        except EmptyServiceField as e:
            form = ConvertFilesForm()
            return TemplateResponse(
                request, "convert/home.html", {'form': form, 'error': e}
            )

    form = ConvertFilesForm()
    return TemplateResponse(
        request, "convert/home.html", {'form': form}
    )


def download(request, file):
    file_path = os.path.join(settings.TMP_FINAL_FILE_LOC, file)
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
