from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from core import utils


class Command(BaseCommand):
    help = 'Restore db from s3'

    option_list = BaseCommand.option_list + (
        make_option('--file',
                    help='The database file to restore is not given the latest file to upload is restored'
        ),
    )

    def handle(self, *args, **options):
        settings = options.get('settings')

        file_to_upload = options.get('file')
        if not settings:
            raise CommandError("settings parameter not provided")
        self.stdout.write("stating to restore")
        utils.restore_db(file_to_upload)
        self.stdout.write('Done restoring db\n')