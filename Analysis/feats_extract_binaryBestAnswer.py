# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.feats_extract_binaryBestAnswer

This script reads a src file containing threads with accepted answers.
Each datapoint is flagged with 1 if it's a best/accepted answer, 0 otherwise.
Output datapoints are grouped by thread.
"""

import json
import glob
import os

from bs4 import BeautifulSoup
import nltk
import dask.bag as db
import dask

from Analysis.Features import text_style

nltk.data.path.append('venv/nltk_data')
dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')

#TODO add other funcs
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

    return {
        'thread_id': thread['thread_id'],
        'question_body': question_body,
        'question_body_stripped': question_body_stripped,
        'accepted_answer_body': accepted_answer_body,
        'accepted_answer_body_stripped': accepted_answer_body_stripped,
        'other_answers_body': other_answers_body,
        'other_answers_body_stripped': other_answers_body_stripped
    }

def thread_extract(thread):
    thread_dataset = []
    # extract accepted_answer feats
    datapoint = dict()
    for f in UNARY_FUNCS:
        datapoint[f.__name__] = f(thread['accepted_answer_body_stripped'])
    datapoint['best_answer'] = 1
    datapoint['thread_id'] = thread['thread_id']
    thread_dataset.append(datapoint)

    # extract other_answers feats
    for answer in thread['other_answers_body_stripped']:
        datapoint = dict()
        for f in UNARY_FUNCS:
            datapoint[f.__name__] = f(answer)
        datapoint['best_answer'] = 0
        datapoint['thread_id'] = thread['thread_id']
        thread_dataset.append(datapoint)
    return thread_dataset

def main():
    # list of delayed values
    bag = db.read_text(SRC_FILE_PATH).map(json.loads, encoding='utf-8')

    # bag has just one item
    for data_list in bag:
        threads = db.from_sequence(data_list, npartitions=4)

        # extract text without html tags
        processed_threads = threads.map(load)

        # extract features, flatten result
        dataset = processed_threads.map(thread_extract)\
                                   .concat()  #dask.bag.core.Bag

        ddf = dataset.to_dataframe()

        # create output directory
        if not os.path.exists(OUTPUT_PATH_DIR):
            os.makedirs(OUTPUT_PATH_DIR)

        # clear output folder first
        filelist = glob.glob(OUTPUT_PATH_DIR + "*.part")
        for f in filelist:
            os.remove(f)

        # always use utf-8
        ddf.to_csv(OUTPUT_PATH_DIR + '.csv', encoding='utf-8')

if __name__ == "__main__":
    main()