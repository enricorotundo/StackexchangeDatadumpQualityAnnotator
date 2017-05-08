# -*- coding: utf-8 -*-

"""
This file clears the annotation columns of the remote databases.
Run it with extreme care.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from ...models import *

class Command(BaseCommand):
    help = 'restore annotations and counts to their default values'

    def handle(self, *args, **options):
        self.stdout.write('Restoring all databases...')

        databases = ['cooking', 'travel', 'webapps']

        for db in databases:
            self.stdout.write(db)

            # restore counting table
            ann = Annotationscount.objects.using(db).get(id=0)
            ann.enrico = 0
            ann.marit = 0
            ann.christine = 0
            ann.henrik = 0
            ann.save()

            # restore annotated Posts
            default_vals = {
                'annotatedqualityenrico' : None,
                'annotatedqualitymarit' : None,
                'annotatedqualitychristine' : None,
                'annotatedqualityhenrik' : None
            }

            Posts.objects.using(db).filter(Q(annotatedqualityenrico__isnull=False) | \
                                           Q(annotatedqualitymarit__isnull=False) | \
                                           Q(annotatedqualitychristine__isnull=False) | \
                                           Q(annotatedqualityhenrik__isnull=False))\
                .update(**default_vals)

        self.stdout.write('DONE!')
