import datetime
import inspect
import logging

from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'static'


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


def upload_media_to_s3(filename, local_file_loc, s3_loc, directory):
    from django.conf import settings
    import os
    import boto3
    from boto3.s3.transfer import S3Transfer
    from boto3.exceptions import S3UploadFailedError

    transfer = S3Transfer(boto3.client('s3',
                                       aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY))
    client = boto3.client('s3')

    local_path = os.path.join(f'{local_file_loc}/', filename)
    s3_path = os.path.join(s3_loc)

    # As of now, we only want to give access to the .csv files
    # Everything else should be private only accessible on our domain
    try:
        if filename.endswith('.csv'):
            transfer.upload_file(local_path, settings.AWS_STORAGE_BUCKET_NAME,
                                 s3_path, extra_args={'ACL': 'public-read'})
            # Since its been uploaded to S3, we can delete the tmp
            # Only needed for production
            os.remove(local_path)
            print(f'{settings.MEDIA_URL}{directory}/{filename}')
            return f'{settings.MEDIA_URL}{directory}/{filename}'
        else:
            transfer.upload_file(local_path, settings.AWS_STORAGE_BUCKET_NAME, s3_path)
            # Since its been uploaded to S3, we can delete the tmp
            # Only needed for production
            os.remove(local_path)
            print( f'{settings.MEDIA_URL}{directory}/{filename}')
            return f'{settings.MEDIA_URL}{directory}/{filename}'
    except S3UploadFailedError as e:
        raise S3UploadFailedError(e)
    except Exception as e:
        print("{} : {}-->{}".format(datetime.datetime.now(), inspect.stack()[0][3], e))
        inspect.stack()
        raise Exception(e)

