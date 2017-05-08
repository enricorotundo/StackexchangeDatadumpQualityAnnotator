# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_users

This script extract users data from the whole DB (important!) and load them into a JSON file.
Works with StackExchange data dumps.
JSON file is encoded in UTF-8 format.
"""

import io
import json

import django
django.setup()
from django.db.models import Count
from django.core.management.base import BaseCommand

from DatasetAnnotator.models import Posts

# community selection
db = 'travel'
OUTPUT_PATH = 'Analysis/Data/' + db + '/'
FILE_NAME = 'users_activity.json'

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        """
        Extract users data to JSON file
        """
        # get all users, not just those in threads with accepted answer
        users = Posts.objects.using(db)\
            .filter(posttypeid__in=[1, 2])\
            .values('owneruserid')\
            .annotate(posts=Count('owneruserid'))\
            .values('owneruserid', 'posts')

        users_dict = dict()
        foo_ = [users_dict.update({d['owneruserid']: {u'nr_posts': d['posts']}}) for d in users]

        with io.open(OUTPUT_PATH + FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(json.dumps(users_dict, ensure_ascii=False))
