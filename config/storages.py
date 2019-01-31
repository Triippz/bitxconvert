from boto3.exceptions import S3UploadFailedError
from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = 'static'


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


def upload_media_to_s3(file, filename, local_file_loc, s3_loc):
    from django.conf import settings
    import os
    import boto3
    from boto3.s3.transfer import S3Transfer

    transfer = S3Transfer(boto3.client('s3',
                                       aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY))
    client = boto3.client('s3')

    local_path = os.path.join(f'{local_file_loc}/', filename)
    s3_path = os.path.join(s3_loc)

    # As of now, we only want to give access to the .csv files
    # Everything else should be private only accessible on our domain
    try:
        if file.endswith('.csv'):
            transfer.upload_file(local_path, settings.AWS_STORAGE_BUCKET_NAME,
                                 s3_path, extra_args={'ACL': 'public-read'})
            # Since its been uploaded to S3, we can delete the tmp
            # Only needed for production
            os.remove(local_path)
        else:
            transfer.upload_file(local_path, settings.AWS_STORAGE_BUCKET_NAME, s3_path)
            # Since its been uploaded to S3, we can delete the tmp
            # Only needed for production
            os.remove(local_path)
    except S3UploadFailedError as e:
        raise S3UploadFailedError(e)
