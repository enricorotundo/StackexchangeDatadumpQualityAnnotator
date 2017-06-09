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
        Extract users' data to JSON file
        """
        users_dict = dict()  # stores the output

        # get all users, not just those in threads with accepted answer
        users = Posts.objects.using(db)\
            .all()\
            .filter(posttypeid__in=[1, 2])\
            .values('owneruserid')\
            .annotate(nr_posts=Count('owneruserid'))\
            .values('owneruserid', 'nr_posts')

        # count the nr of posts for each user
        _ = [users_dict.update({d['owneruserid']: {u'nr_posts': d['nr_posts']}}) for d in users]

        accepted_answer_ids = Posts.objects.using(db) \
            .all() \
            .filter(posttypeid__in=[1, 2]) \
            .values_list('acceptedanswerid') \
            .distinct()

        # count the nr of accepted answers for each user
        users_w_best_answers = Posts.objects.using(db)\
            .all() \
            .filter(posttypeid__in=[1, 2], id__in=accepted_answer_ids) \
            .values('owneruserid') \
            .annotate(nr_bestanswers=Count('owneruserid'))

        _ = [users_dict[d['owneruserid']].update({u'nr_bestanswers': d['nr_bestanswers']}) for d in users_w_best_answers]


        with io.open(OUTPUT_PATH + FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(json.dumps(users_dict, ensure_ascii=False))
