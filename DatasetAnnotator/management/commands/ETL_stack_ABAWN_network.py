# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_ABAWN_network

This script extract an Asker-best answerer weighted network (ABAWN) from the whole DB (important!) and save it into a GRAPHML file.
Works with StackExchange data dumps.
Output file is encoded in UTF-8 format.
"""

import itertools

import django
import networkx as nx
import numpy as np

from django.core.management.base import BaseCommand
from DatasetAnnotator.models import Posts

django.setup()

# community selection
db = 'travel'
#db = 'stackoverflow'

OUTPUT_PATH = 'Analysis/Data/' + db + '/'
FILE_NAME = 'asker_best_answerer_weighted_network.graphml'


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        # all the Q&As of the whole dataset!
        questions = Posts.objects.using(db).filter(posttypeid=1)
        all_answers = Posts.objects.using(db).filter(posttypeid=2)

        # list of tuples of IDs
        edges = list()

        for question in questions:
            # get best answer
            best_answer_id = question.acceptedanswerid
            answers = all_answers.filter(parentid=question.id)\
                .filter(id=best_answer_id)
            # get IDs of users who answered with the best answer
            users = list(answers.values_list('owneruserid', flat=True))
            # replacing deleted users (None to -1)
            users = [user if user is not None else -1L for user in users]
            users = [i for i in itertools.product([question.owneruserid if question.owneruserid else -1], users)]

            # add node weight info
            if users:
                weight = float(np.log2(all_answers.filter(parentid=question.id).count() + 1))
                users = [(tuple[0], tuple[1], {'weight': weight}) for tuple in users]

            if users:
                edges.extend(users)

        # create graph
        g = nx.MultiDiGraph()
        g.add_edges_from(edges)

        # save graph on disk
        nx.write_graphml(g, OUTPUT_PATH + FILE_NAME, encoding='utf-8', prettyprint=True)
