# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_users

This script extract users data from the whole DB (important!) and load them into a JSON file.
Works with StackExchange data dumps.
JSON file is encoded in UTF-8 format.
"""

import io
import json
import datetime

import pytz
import django
django.setup()
from django.db.models import Count
from django.core.management.base import BaseCommand

from DatasetAnnotator.models import *

# database selection
db = 'travel'
#db = 'stackoverflow'

OUTPUT_PATH = 'Analysis/Data/' + db + '/'
FILE_NAME = 'users_activity.json'

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        """
        Extract users' data to JSON file
        NOTE: users_dict should not present any missing value so every user should have all fields!
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
        [users_dict.update({d['owneruserid']: {u'nr_posts': d['nr_posts']}}) for d in users]

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

        [users_dict[d['owneruserid']].update({u'nr_bestanswers': d['nr_bestanswers']}) for d in users_w_best_answers]
        # fill in zeros when user has no bestanswer
        map(lambda key: users_dict[key].update({u'nr_bestanswers': 0}) if 'nr_bestanswers' not in users_dict[key] else None, users_dict)

        # extract the nr of days since duration
        dates = Users.objects.using(db) \
            .all() \
            .filter(id__in=users_dict.keys()) \
            .values('id', 'creationdate')

        [users_dict[d['id']].update({'nr_days_since_signup': (datetime.datetime(2017,1,6,0,0,0,0, tzinfo=pytz.utc) - d['creationdate']).days}) for d in dates]

        with io.open(OUTPUT_PATH + FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(json.dumps(users_dict, ensure_ascii=False))
