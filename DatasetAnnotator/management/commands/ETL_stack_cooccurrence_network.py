# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_cooccurrence_network

This script extract a co-occurrences network from the whole DB (important!) and save it into a graphml file.
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
#db = 'stackoverflow'

OUTPUT_PATH = 'Analysis/Data/' + db + '/'
FILE_NAME = 'cooccurrence_network.graphml'


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        # all the Q&As of the whole dataset!
        questions = Posts.objects.using(db).filter(posttypeid=1)
        all_answers = Posts.objects.using(db).filter(posttypeid=2)

        # list of tuples
        edges = list()

        for question in questions:
            answers = all_answers.filter(parentid=question.id)
            # get IDs of users in the discussion
            users = list(answers.values_list('owneruserid', flat=True))
            # get ID of the questioner
            users.append(question.owneruserid if question.owneruserid else -1)
            # replacing deleted users (None to -1)
            users = [user if user is not None else -1L for user in users]
            edges.extend([i for i in itertools.combinations(users, 2)])

        # create graph
        g = nx.MultiGraph()
        g.add_edges_from(edges)

        # save graph on disk
        nx.write_graphml(g, OUTPUT_PATH + FILE_NAME, encoding='utf-8', prettyprint=True)
