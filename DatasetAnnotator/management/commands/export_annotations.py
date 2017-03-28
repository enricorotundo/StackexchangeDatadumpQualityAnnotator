from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from ...models import *
import csv, datetime
from django.db.models import Q

class Command(BaseCommand):
    help = 'Export annotations in a CSV file'

    def handle(self, *args, **options):
        self.stdout.write('Exporting annotations')

        #databases = ['cooking', 'travel', 'webapps']
        databases = ['travel']

        for db in databases:
            file_name = '{}_Posts_{}.csv'.format(db, datetime.datetime.utcnow().isoformat())
            print file_name

            annotations_dict = Posts.objects.using(db) \
                                    .filter(Q(annotatedqualityenrico__isnull=False) | \
                                            Q(annotatedqualitymarit__isnull=False) | \
                                            Q(annotatedqualitychristine__isnull=False) | \
                                            Q(annotatedqualityhenrik__isnull=False)) \
                                    .values('id',\
                                           'annotatedqualityenrico',\
                                           'annotatedqualitymarit', \
                                           'annotatedqualitychristine',\
                                           'annotatedqualityhenrik')
            keys = annotations_dict[0].keys()

            with open('annotations_backups/' + file_name, 'wb') as csvfile:
                dict_writer = csv.DictWriter(csvfile, keys)
                dict_writer.writeheader()
                dict_writer.writerows(annotations_dict)
