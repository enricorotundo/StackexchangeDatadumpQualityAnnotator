# -*- coding: utf-8 -*-

"""
Run this with: time python manage.py ETL_stack_CBEN_network

This script extract an Competition-based expertise network from the whole DB (important!) and save it into a GRAPHML file.
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
FILE_NAME = 'competition_based_expertise_network.graphml'


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
            best_answer = all_answers\
                .filter(parentid=question.id)\
                .filter(id=question.acceptedanswerid)
            # get IDs of users who answered with the best answer
            best_user = list(best_answer.values_list('owneruserid', flat=True))

            # get all other users in the discussion
            other_users = list(all_answers.filter(parentid=question.id).values_list('owneruserid', flat=True))
            # remove best answerer
            for user in best_user:
                other_users.remove(user)

            # replacing deleted users (None to -1)
            other_users = [user if user is not None else -1L for user in other_users]
            best_user = [user if user is not None else -1L for user in best_user]
            # connecting other users -> best answerer
            users = [i for i in itertools.product(other_users, best_user)]

            if users:
                edges.extend(users)

        # create graph
        g = nx.MultiDiGraph()
        g.add_edges_from(edges)

        # save graph on disk
        nx.write_graphml(g, OUTPUT_PATH + FILE_NAME, encoding='utf-8', prettyprint=True)
