import json
from urllib.request import urlopen, URLError

from django.core.management.base import BaseCommand, CommandError
from ...models import ZipcodeMapping


# https://www.data.gouv.fr/en/datasets/codes-postaux/
DEFAULT_JSON_URL = 'https://www.data.gouv.fr/en/datasets/r/34d4364c-22eb-4ac0-b179-7a1845ac033a'

class Command(BaseCommand):
    help = 'Import french zipcodes into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json-url',
            default=DEFAULT_JSON_URL,
            help="Must follow the format of this data : https://www.data.gouv.fr/en/datasets/codes-postaux/",
        )

    def handle(self,  json_url, **options):
        print('Fetching zipcodes for FRANCE from {}'.format(json_url))
        ZipcodeMapping.objects.all().delete()
        try:
            response = json.loads(urlopen(json_url).read().decode('utf-8'))
        except URLError:
            raise CommandError('Cannot fetch {}'.format(json_url))

        mappings_data = [
            {'zipcode': row['codePostal'], 'city': row['nomCommune']}
            for row in response
        ]
        print('Inserting zipcodes into database {}'.format(json_url))
        ZipcodeMapping.objects.bulk_create(
            [
                ZipcodeMapping(**entry)
                for entry in mappings_data
            ]
        )
        print('Done')
