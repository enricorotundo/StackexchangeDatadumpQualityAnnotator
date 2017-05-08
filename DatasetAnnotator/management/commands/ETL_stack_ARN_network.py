# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_ARN_network

This script extract an Asker-Replier (ARN) network from the whole DB (important!) and save it into a GRAPHML file.
Works with StackExchange data dumps.
Output file is encoded in UTF-8 format.
"""

import itertools

import django
import networkx as nx

from django.core.management.base import BaseCommand
from DatasetAnnotator.models import Posts

django.setup()

# community selection
db = 'travel'
OUTPUT_PATH = 'Analysis/Data/' + db + '/'
FILE_NAME = 'asker_replier_network.graphml'


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        # all the Q&As of the whole dataset!
        questions = Posts.objects.using(db).filter(posttypeid=1)
        all_answers = Posts.objects.using(db).filter(posttypeid=2)

        # list of tuples of IDs
        edges = list()

        for question in questions:
            answers = all_answers.filter(parentid=question.id)
            # get IDs of users in the discussion
            users = list(answers.values_list('owneruserid', flat=True))
            # replacing deleted users (None to -1)
            users = [user if user is not None else -1L for user in users]
            edges.extend([i for i in itertools.product([question.owneruserid if question.owneruserid else -1], users)])

        # create graph
        g = nx.MultiDiGraph()
        g.add_edges_from(edges)

        # save graph on disk
        nx.write_graphml(g, OUTPUT_PATH + FILE_NAME, encoding='utf-8', prettyprint=True)
