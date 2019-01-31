import os

from django.conf import settings

from bitxconvert.convert.utils.exchanges.binance import get_binance_version
from bitxconvert.convert.utils.exchanges.bittrex import get_bittrex_version
from bitxconvert.convert.utils.exchanges.coinbase import get_coinbase_version
from bitxconvert.convert.utils.services.bitcointax import get_bitcointax_version
from bitxconvert.convert.utils.services.cointracker import get_cointracker_version
from bitxconvert.convert.models import Conversion
from bitxconvert.convert.utils.services.cryptotrader import get_cryptotrader_version
from bitxconvert.convert.utils.services.manual import get_manual_version
from bitxconvert.users.models import User



def get_exchange(text):
    for exchange in settings.CONVERT_EXCHANGES:
        if exchange in text:
            return exchange


def get_service(text):
    for service in settings.CONVERT_SERVICES:
        if service in text:
            return service


def create_record(exchange, service, files, final_file_results, user=None):
    from django.conf import settings

    if settings.DEBUG:
        if user.is_anonymous:
            conversion = Conversion.objects.create(
                number_of_files=len(files),
                exchange=exchange,
                tax_service=service,
                trades_processed=final_file_results['total_orders'],
                file_name=final_file_results['file_name']
            )
            conversion.save()
            final_file_results['file'].close()
            return conversion
        else:
            conversion = Conversion.objects.create(
                number_of_files=len(files),
                exchange=exchange,
                tax_service=service,
                trades_processed=final_file_results['total_orders'],
                user=User.objects.get(pk=user.id),
                file_name=final_file_results['file_name']
            )
            conversion.save()
            final_file_results['file'].close()
            return conversion
    else:
        from config.settings.production import MediaRootS3Boto3Storage

        if user.is_anonymous:
            conversion = Conversion.objects.create(
                number_of_files=len(files),
                exchange=exchange,
                tax_service=service,
                trades_processed=final_file_results['total_orders'],
                file_name=final_file_results['file_name'],
            )
            conversion.file(storage=MediaRootS3Boto3Storage(), file=final_file_results['file'])
            conversion.save()
            final_file_results['file'].close()
            # Since its been uploaded to S3, we can delete the tmp
            # Only needed for production
            os.remove(final_file_results['file_path'])
            return conversion
        else:
            conversion = Conversion.objects.create(
                number_of_files=len(files),
                exchange=exchange,
                tax_service=service,
                trades_processed=final_file_results['total_orders'],
                user=User.objects.get(pk=user.id),
                file_name=final_file_results['file_name'],
            )
            conversion.file(storage=MediaRootS3Boto3Storage(), file=final_file_results['file'])
            conversion.save()
            final_file_results['file'].close()
            # Since its been uploaded to S3, we can delete the tmp
            # Only needed for production
            os.remove(final_file_results['file_path'])
            return conversion


def parse_files(exchange_in, service_in, files, user=None):
    exchange = get_exchange(exchange_in)
    service = get_service(service_in)

    file_info = {}

    # Let's parse the file(s) into a new file based off the exchange
    if exchange == "BITTREX":
        file_info = get_bittrex_version(files)
    elif exchange == "BINANCE":
        file_info = get_binance_version(files)
    elif exchange == "COINBASE":
        file_info = get_coinbase_version(files)

    # Now let's modify that new file into the format needed by the service chosen
    final_file_results = ""
    if service == "MANUAL":
        final_file_results = get_manual_version(file_info, exchange)
    elif service == "CRYPTOTRADER":
        final_file_results = get_cryptotrader_version(file_info, exchange)
    elif service == "BITCOINTAX":
        final_file_results = get_bitcointax_version(file_info, exchange)
    elif service == "COINTRACKER":
        final_file_results = get_cointracker_version(file_info)

    if user is None:
        conversion = create_record(exchange, service, files, final_file_results)
    else:
        conversion = create_record(exchange, service, files, final_file_results, user)

    return {
        'conversion': conversion,
        'results': final_file_results
    }
