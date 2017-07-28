# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.network_analysis

This script reads a bunch of graphml files and outputs a pickled dict (??).
Keys are user ids and values are corresponding values from the network analysis.
"""

import logging

import networkx as nx
import pandas as pd

from Utils import settings as settings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

db = 'travel'
FILES_PATH = 'Analysis/Data/' + db + '/'
CON_FILE_NAME = 'cooccurrence_network.graphml'
CBEN_FILE_NAME = 'competition_based_expertise_network.graphml'
ARN_FILE_NAME = 'asker_replier_network.graphml'
ABAN_FILE_NAME = 'asker_best_answerer_network.graphml'
ABAWN_FILE_NAME = 'asker_best_answerer_weighted_network.graphml'
OUTPUT_FILE_NAME = 'network_analysis.csv'

def main():
    logging.info('Network analysis: started.')

    param_pagerank = {
        'alpha': 0.9,
        'max_iter': 10000,
        'tol': 1e-06
    }

    param_hits = {
        'max_iter': 10000,
        'tol': 1e-06
    }

    data_dict = dict()

    # co-occurrences
    logging.info('Analysing COOCN.')
    g = nx.read_graphml(FILES_PATH + CON_FILE_NAME, node_type=long)
    # remove user -1
    g.remove_node(-1)
    data_dict['cooccurrence_degree_centrality'] = nx.degree_centrality(g)
    # the following 2 takes about 50 mins
    data_dict['cooccurrence_closeness_centrality'] = nx.closeness_centrality(g)
    data_dict['cooccurrence_betweenness_centrality'] = nx.betweenness_centrality(g)

    # ARN
    logging.info('Analysing ARN.')
    g = nx.read_graphml(FILES_PATH + ARN_FILE_NAME, node_type=long)
    # remove user -1
    g.remove_node(-1)
    data_dict['ARN_indegree'] = g.in_degree()
    data_dict['ARN_pagerank'] = nx.pagerank_scipy(g, **param_pagerank)
    data_dict['ARN_hits_hubs'] = nx.hits_scipy(g, **param_hits)[0]
    data_dict['ARN_hits_authority'] = nx.hits_scipy(g, **param_hits)[1]

    # CBEN
    logging.info('Analysing CBEN.')
    g = nx.read_graphml(FILES_PATH + CBEN_FILE_NAME, node_type=long)
    # remove user -1
    g.remove_node(-1)
    data_dict['CBEN_indegree'] = g.in_degree()
    data_dict['CBEN_pagerank'] = nx.pagerank_scipy(g, **param_pagerank)
    data_dict['CBEN_hits_hubs'] = nx.hits_scipy(g, **param_hits)[0]
    data_dict['CBEN_hits_authority'] = nx.hits_scipy(g, **param_hits)[1]

    # ABAN
    logging.info('Analysing ABAN.')
    g = nx.read_graphml(FILES_PATH + ABAN_FILE_NAME, node_type=long)
    # remove user -1
    g.remove_node(-1)
    data_dict['ABAN_indegree'] = g.in_degree()
    data_dict['ABAN_pagerank'] = nx.pagerank_scipy(g, **param_pagerank)
    data_dict['ABAN_hits_hubs'] = nx.hits_scipy(g, **param_hits)[0]
    data_dict['ABAN_hits_authority'] = nx.hits_scipy(g, **param_hits)[1]

    # ABAWN
    logging.info('Analysing ABAWN.')
    g = nx.read_graphml(FILES_PATH + ABAWN_FILE_NAME, node_type=long)
    # remove user -1
    g.remove_node(-1)
    data_dict['ABAWN_indegree'] = g.in_degree()
    data_dict['ABAWN_pagerank'] = nx.pagerank_scipy(g, **param_pagerank)
    data_dict['ABAWN_hits_hubs'] = nx.hits_scipy(g, **param_hits)[0]
    data_dict['ABAWN_hits_authority'] = nx.hits_scipy(g, **param_hits)[1]

    logging.info('Buidling DataFrame and saving...')
    df = pd.DataFrame.from_dict(data_dict)
    # fill missing values with 0
    #df.fillna(0, inplace=True)
    # fill missing values with Mean
    df.fillna(df.mean(), inplace=True)
    df.to_csv(FILES_PATH + OUTPUT_FILE_NAME, encoding='utf-8')
    logging.info('Done.')
    logging.info('Network analysis: finished.')

if __name__ == "__main__":
    main()
