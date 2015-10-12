from django.core import management
from django.conf import settings
from boto.s3.connection import S3Connection
import os

__author__ = 'mwas'


def backup_db():
    django_settings = os.environ['DJANGO_SETTINGS_MODULE']

    management.call_command('dbbackup', settings=django_settings)
    media_backup()


def restore_db(file_to_upload=None):
    # if file is not provided restore the latest file loaded
    if not file_to_upload:
        # find the last db file backed up
        conn = S3Connection(settings.DBBACKUP_S3_ACCESS_KEY, settings.DBBACKUP_S3_SECRET_KEY)
        sauti_bucket = conn.get_bucket(settings.DBBACKUP_S3_BUCKET
        )
        keys = sauti_bucket.list(prefix="django-dbbackups")
        psql_files = filter(lambda key: "psql" in key.name, keys)

        # find the latest file
        file_to_upload = psql_files[-1].name

    management.call_command('dbrestore', filepath=file_to_upload, database='default', )


def media_backup():
    management.call_command('backup_media')