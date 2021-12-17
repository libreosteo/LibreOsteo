import json
from urllib.request import urlopen, URLError

from django.core.management.base import BaseCommand, CommandError
from ...models import ZipcodeMapping

# https://www.data.gouv.fr/en/datasets/codes-postaux/
DEFAULT_JSON_URL = 'https://www.data.gouv.fr/en/datasets/r/34d4364c-22eb-4ac0-b179-7a1845ac033a'


class Command(BaseCommand):
    help = 'Import french zipcodes into database'

    def add_arguments(self, parser):

        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            '--json-url',
            default=DEFAULT_JSON_URL,
            help=
            "Must follow the format of this data : https://www.data.gouv.fr/en/datasets/codes-postaux/",
        )
        group.add_argument(
            '--json-file',
            default=None,
            help=
            "Must follow the format of this data : https://www.data.gouv.fr/en/datasets/codes-postaux/",
        )

        parser.add_argument(
            '--download-only',
            action="store_true",
            default=False,
            help=
            "Download the default dataset from the list of zipcode for France")

    def handle(self, json_url, json_file, **options):
        print('Fetching zipcodes for FRANCE from {}'.format(json_file
                                                            or json_url))
        if options['download_only']:
            open("zipcode_dataset.json",
                 "w").write(urlopen(json_url).read().decode('utf-8'))
            print("Done")
            return
        if json_file:
            try:
                response = json.load(open(json_file, encoding='utf-8'))
            except OSError:
                raise CommandError('Cannot read {}'.format(json_file))

        else:
            try:
                response = json.loads(urlopen(json_url).read().decode('utf-8'))
            except URLError:
                raise CommandError('Cannot fetch {}'.format(json_url))

        mappings_data = [{
            'zipcode': row['codePostal'],
            'city': row['nomCommune']
        } for row in response]
        print('Inserting zipcodes into database from {} {}'.format(
            'file' if json_file else 'URL', json_file or json_url))
        ZipcodeMapping.objects.all().delete()
        ZipcodeMapping.objects.bulk_create(
            [ZipcodeMapping(**entry) for entry in mappings_data])
        print('Done')
