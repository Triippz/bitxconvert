from django.conf import settings


def validate_convert(post, file_request):
    try:
        if post["exchange"] is None:
            return False, "You must select an exchange"
    except:
        return False, "You must select an exchange"

    try:
        if post["convert"] is None:
            return False, "You must select a service"
    except:
        return False, "You must select a service"

    files = file_request.getlist('file_field')
    for file in files:
        if not any(file.name.endswith(extension) for extension in settings.CONVERT_FILE_TYPES):
            return False, "File {}, does not a proper file type. Proper file types are: {}" \
                .format(file, settings.CONVERT_FILE_TYPES)

    return True, ""
