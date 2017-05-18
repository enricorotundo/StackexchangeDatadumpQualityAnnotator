# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.feats_extract

This script reads a src file containing threads with accepted answers.
Each datapoint is flagged with 1 if it's a best/accepted answer, 0 otherwise.
Output datapoints are indexed by thread_id.
"""

import json
import logging
import argparse

import numpy as np
from bs4 import BeautifulSoup
import nltk
import dask.bag as db
import dask.multiprocessing
from dask.diagnostics import ProgressBar
import pandas as pd

from Analysis.Features import text_style
from Utils.settings import Settings
from Utils.commons import prepare_folder




# TODO add other funcs
UNARY_FUNCS = [text_style.ty_cpc,
               text_style.ty_cpe,
               text_style.ty_poc,
               text_style.ty_pde,
               text_style.ty_sde,
               text_style.ty_nwnt,
               text_style.ty_typo,
               text_style.ty_slp,
               text_style.ty_avc,
               text_style.ty_pc,
               text_style.ty_pvc,
               text_style.ty_cjr,
               text_style.ty_nr,
               text_style.ty_pr,
               text_style.ty_ber,
               text_style.ty_sp,
               text_style.ty_sa,
               text_style.ty_scc,
               text_style.ty_sscc,
               text_style.ty_sipc,
               text_style.ty_spr,
               ]



#TODO add other funcs + call them in thread_extract()
BINARY_FUNCS = []


def load(thread):
    """
    Given a thread dict, it filters fields and add html-stripped body text.
    """
    # read question
    question_body = thread['question']['body']
    question_body_stripped = BeautifulSoup(question_body, "html5lib").get_text()

    # read accepted_answer
    accepted_answer_body = thread['accepted_answer']['body']
    accepted_answer_body_stripped = BeautifulSoup(accepted_answer_body, "html5lib").get_text()

    # read other_answers
    other_answers_body = [answer['body'] for answer in thread['other_answers']]
    other_answers_body_stripped = [BeautifulSoup(answer_body, "html5lib").get_text()
                                   for answer_body in other_answers_body]
    other_answers_users_ids = [answer['user'] for answer in thread['other_answers']]
    other_answers_post_ids = [answer['post_id'] for answer in thread['other_answers']]

    return {
        'thread_id': thread['thread_id'],
        'question_body': question_body,
        'question_body_stripped': question_body_stripped,
        'question_user_id': thread['question']['user'],
        'question_post_id': thread['question']['post_id'],

        'accepted_answer_body': accepted_answer_body,
        'accepted_answer_body_stripped': accepted_answer_body_stripped,
        'accepted_answer_user_id': thread['accepted_answer']['user'],
        'accepted_answer_post_id': thread['accepted_answer']['post_id'],

        'other_answers_body': other_answers_body,
        'other_answers_body_stripped': other_answers_body_stripped,
        'other_answers_users_ids': other_answers_users_ids,
        'other_answers_post_ids': other_answers_post_ids,
    }


def thread_extract(thread):
    """
    Extracts features and returns a list of data-points for the given thread.  
    """
    thread_dataset = []

    # ACCEPTED ANSWER
    # ignore posts by 'null' users
    if thread['accepted_answer_user_id']:
        # extract unary features
        datapoint = dict()
        for f in UNARY_FUNCS:
            datapoint[f.__name__] = f(thread['accepted_answer_body_stripped'])

        # add network analysis features
        df_net_accepted_answer = df_network_analysis.loc[thread['accepted_answer_user_id']]  # use 'loc' not 'iloc'!
        for col_name, values in df_net_accepted_answer.iteritems():
            datapoint[col_name] = values

        # add user's activity features
        df_user_activity_accepted_answer = df_users_activity.loc[thread['accepted_answer_user_id']]  # use 'loc' not 'iloc'!
        for col_name, values in df_user_activity_accepted_answer.iteritems():
            datapoint[col_name] = values

        # add additional data
        datapoint['best_answer'] = 1
        datapoint['thread_id'] = thread['thread_id']
        datapoint['post_id'] = thread['accepted_answer_post_id']

        # append datapoint
        thread_dataset.append(datapoint)

    # OTHER ANSWERS FEATURES
    for answer, user_id, post_id in zip(thread['other_answers_body_stripped'],
                                        thread['other_answers_users_ids'],
                                        thread['other_answers_post_ids']):
        # ignore posts by 'null' users
        if user_id:
            datapoint = dict()

            # extract unary features
            for f in UNARY_FUNCS:
                datapoint[f.__name__] = f(answer)

            # add network analysis features
            df_net_answer = df_network_analysis.loc[user_id]  # use 'loc' not 'iloc'!
            for col_name, values in df_net_answer.iteritems():
                datapoint[col_name] = values

            # add user's activity features
            df_user_activity_answer = df_users_activity.loc[user_id]  # use 'loc' not 'iloc'!
            for col_name, values in df_user_activity_answer.iteritems():
                datapoint[col_name] = values

            # add additional data
            datapoint['best_answer'] = 0
            datapoint['thread_id'] = thread['thread_id']
            datapoint['post_id'] = post_id

            # append datapoint
            thread_dataset.append(datapoint)

    return thread_dataset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--n_partitions', type=int)
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--task_name', type=str, required=True)
    parser.add_argument('--src_file_name', type=str, required=True)
    args = parser.parse_args()

    settings = Settings(args.db, args.task_name, args.src_file_name)

    logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

    # setup NLTK
    nltk.data.path.append(settings.NLTK_DATA_PATH)

    dask.set_options(get=dask.multiprocessing.get)

    # prepare network analysis data
    global df_network_analysis
    df_network_analysis = pd.read_csv(settings.DATA_DIR_PATH + '/network_analysis.csv', encoding=settings.ENCODING)
    df_network_analysis.set_index('Unnamed: 0', inplace=True)  # indexes must be the one in the CSV (ie. user_ids)

    # prepare users activity data
    global df_users_activity
    df_users_activity = pd.read_json(settings.DATA_DIR_PATH + '/users_activity.json', orient='index',
                                     encoding=settings.ENCODING)
    df_users_activity.sort_index(inplace=True)
    df_users_activity = df_users_activity[:-1]  # get rid of the 'null' user so can convert index to int64
    df_users_activity.index = df_users_activity.index.astype(np.int64)  # indexes are user_ids

    logging.info('Features extraction: started.')
    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):

        # list of delayed values
        bag = db.read_text(settings.SRC_FILE_PATH)\
            .map(json.loads, encoding=settings.ENCODING)

        # bag has just one item!
        for data_list in bag:

            if args.draft:
                logging.info('Draft mode enabled, using just a sampled dataset.')
                data_list = data_list[:5]  # get only some threads
            else:
                logging.info('Draft mode disabled, using whole datasource.')
                logging.debug(len(data_list))

            threads = db.from_sequence(data_list, npartitions=args.n_partitions)

            # extract text without html tags
            processed_threads = threads.map(load)

            # extract features, flatten result
            dataset = processed_threads.map(thread_extract).concat()  # dask.bag.core.Bag

            # prepare output directory
            if args.draft:
                prepare_folder(settings.OUTPUT_PATH_DIR_DRAFT)
            else:
                prepare_folder(settings.OUTPUT_PATH_DIR)

            df = dataset.to_dataframe()

            # make sure partitions take thread_id into account!
            df = df.set_index('thread_id')

            # always use utf-8
            if args.draft:
                df.to_csv(settings.OUTPUT_PATH_DIR_DRAFT + 'features-*.csv', encoding=settings.ENCODING)
            else:
                df.to_csv(settings.OUTPUT_PATH_DIR + 'features-*.csv', encoding=settings.ENCODING)

        logging.info('Features extraction: completed.')

if __name__ == "__main__":
    main()
