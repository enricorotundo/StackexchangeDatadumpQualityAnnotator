# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.feats_extract_binaryBestAnswer

This script reads a src file containing threads with accepted answers.
Each datapoint is flagged with 1 if it's a best/accepted answer, 0 otherwise.
Output datapoints are indexed by thread_id.
"""

import json
import logging

from bs4 import BeautifulSoup
import nltk
import dask.bag as db
import dask.multiprocessing
from dask.diagnostics import ProgressBar
import pandas as pd

from Analysis.Features import text_style
from Utils import settings_binaryBestAnswer as settings
from Utils.commons import prepare_folder

logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)
nltk.data.path.append('venv/nltk_data')
dask.set_options(get=dask.multiprocessing.get)
df_network_analysis = pd.read_csv(settings.DATA_DIR_PATH + '/network_analysis.csv', encoding=settings.ENCODING)
df_users_activity = pd.read_json(settings.DATA_DIR_PATH + '/users_activity.json', orient='index', encoding=settings.ENCODING)

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

    # extract unary features
    datapoint = dict()
    for f in UNARY_FUNCS:
        datapoint[f.__name__] = f(thread['accepted_answer_body_stripped'])

    # add network analysis features
    df_net_accepted_answer = df_network_analysis.iloc[thread['accepted_answer_user_id']]
    for col_name, values in df_net_accepted_answer.iteritems():
        datapoint[col_name] = values

    # add user's activity features
    df_user_activity_accepted_answer = df_users_activity.iloc[thread['accepted_answer_user_id']]
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
        datapoint = dict()

        # extract unary features
        for f in UNARY_FUNCS:
            datapoint[f.__name__] = f(answer)

        # add network analysis features
        df_net_answer = df_network_analysis.iloc[user_id]
        for col_name, values in df_net_answer.iteritems():
            datapoint[col_name] = values

        # add user's activity features
        df_user_activity_answer = df_users_activity.iloc[user_id]
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
    logging.info('Features extraction: started.')
    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):

        # list of delayed values
        bag = db.read_text(settings.SRC_FILE_PATH)\
            .map(json.loads, encoding=settings.ENCODING)

        # bag has just one item!
        for data_list in bag:

            if settings.DRAFT_MODE:
                logging.info('Draft mode enabled, using just a sampled dataset.')
                data_list = data_list[:5]
            else:
                logging.info('Draft mode disabled, using whole datasource.')
                logging.debug(len(data_list))

            threads = db.from_sequence(data_list, npartitions=settings.N_PARTITIONS)

            # extract text without html tags
            processed_threads = threads.map(load)

            # extract features, flatten result
            dataset = processed_threads.map(thread_extract).concat()  # dask.bag.core.Bag

            # prepare output directory
            prepare_folder(settings.OUTPUT_PATH_DIR)

            df = dataset.to_dataframe()

            # make sure partitions take thread_id into account!
            df = df.set_index('thread_id')

            # always use utf-8
            df.to_csv(settings.OUTPUT_PATH_DIR + 'features-*.csv', encoding=settings.ENCODING)

        logging.info('Features extraction: completed.')


if __name__ == "__main__":
    main()
