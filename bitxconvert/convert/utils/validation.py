import datetime
import inspect

from django.conf import settings

from bitxconvert.utils.exceptions import IncorrectFileFormat, EmptyExchangeField, EmptyServiceField


def validate_convert(post, file_request):
    try:
        if post["exchange"] is None:
            return False, "You must select an exchange"
    except Exception as e:
        print("{} -- Error: {} --> {}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
        raise EmptyExchangeField("You must select an exchange")

    try:
        if post["convert"] is None:
            return False, "You must select a service"
    except Exception as e:
        print("{} -- Error: {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
        raise EmptyServiceField("You must select a service")

    files = file_request.getlist('file_field')
    for file in files:
        if post["exchange"] == "BINANCE":
            if not any(file.name.endswith(extension) for extension in settings.BINANCE_CONVERT_FILE_TYPES):
                raise IncorrectFileFormat("File {}, does not a proper file type. Proper file types for BINANCE are: {}" \
                                          .format(file, settings.BINANCE_CONVERT_FILE_TYPES))
        if post["exchange"] == "BITTREX":
            if not any(file.name.endswith(extension) for extension in settings.BITTREX_CONVERT_FILE_TYPES):
                raise IncorrectFileFormat("File {}, does not a proper file type. Proper file types for BITTREX are: {}" \
                                          .format(file, settings.BITTREX_CONVERT_FILE_TYPES))
        if post["exchange"] == "COINBASE":
            if not any(file.name.endswith(extension) for extension in settings.BITTREX_CONVERT_FILE_TYPES):
                raise IncorrectFileFormat("File {}, does not a proper file type. Proper file types for COINBASE are: {}" \
                                          .format(file, settings.COINBASE_CONVERT_FILE_TYPES))

    return True, ""
