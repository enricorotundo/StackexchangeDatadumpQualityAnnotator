# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_threads

This script extract threads with a best/selected answer and load them into a JSON file.
Works with StackExchange data dumps, highly inefficient ;-)
JSON file is encoded in UTF-8 format.
"""


import io
import json

import django
django.setup()
from django.core.management.base import BaseCommand

from DatasetAnnotator.models import *

# community selection
db = 'travel'
OUTPUT_PATH = 'Analysis/Data/' + db + '/'
#FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
#FILE_NAME = 'threads_acceptedOnly_all.json'
FILE_NAME = 'threads_all_all.json'

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        """
        FILE_NAME naming schema, _ separated:
            * threads
            * all / acceptedOnly
            * all / ansCountGte2 / ansCountGte4
        """

        # selecting questions, see above for description
        if FILE_NAME == 'threads_acceptedOnly_all.json':
            questions = Posts.objects.using(db).filter(posttypeid=1) \
                .filter(acceptedanswerid__isnull=False)
        elif FILE_NAME == 'threads_acceptedOnly_ansCountGte2.json':
            questions = Posts.objects.using(db).filter(posttypeid=1) \
                .filter(acceptedanswerid__isnull=False) \
                .filter(answercount__gte=2)
        elif FILE_NAME == 'threads_acceptedOnly_ansCountGte4.json':
            # this filtering is used in most of the papers
            questions = Posts.objects.using(db).filter(posttypeid=1) \
                .filter(acceptedanswerid__isnull=False) \
                .filter(answercount__gte=4)
        elif FILE_NAME == 'threads_all_all.json':
            # this is for AA_dataset_builder
            questions = Posts.objects.using(db).filter(posttypeid=1)

        all_answers = Posts.objects.using(db).filter(posttypeid=2)

        threads = []

        #TODO retrive up/downvotes from "Votes" table

        print 'Nr. of questions selected: {}'.format(questions.count())

        count = 0
        for question in questions:
            count += 1
            if count % 1000 == 0:
                print count

            answers = all_answers.filter(parentid=question.id)

            q = {
                    'title': question.title,
                    'body': question.body,
                    'user': question.owneruserid,
                    'tags': question.tags,
                    'post_id': question.id,
                }

            a = []

            for answer in answers:
                if answer.id != question.acceptedanswerid:
                    a.append({
                        'body': answer.body,
                        'user': answer.owneruserid,
                        'post_id': answer.id
                    })

            try:
                # fails if there's no accepted answer
                accepted_ans = answers.get(id=question.acceptedanswerid)

                # buidling item
                threads.append({
                    'thread_id': question.id,
                    'question': q,
                    'other_answers': a,
                    'accepted_answer': {
                        'body': accepted_ans.body,
                        'user': accepted_ans.owneruserid,
                        'post_id': accepted_ans.id,
                    }
                })
            except:
                # buidling item
                threads.append({
                    'thread_id': question.id,
                    'question': q,
                    'other_answers': a,
                })

        print 'Sample thread: \n{}'.format(threads[0])

        # write in utf-8 encoding
        with io.open(OUTPUT_PATH + FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(json.dumps(threads, ensure_ascii=False))
