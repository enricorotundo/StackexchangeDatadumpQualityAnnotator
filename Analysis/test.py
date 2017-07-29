# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.test

Evaluate over the evaluation set (unseen, left-out).
"""

import logging
import argparse
import pprint

import dask
import dask.multiprocessing
import dask.dataframe as ddf
import pandas as pd

from dask.diagnostics import ProgressBar
from sklearn.externals import joblib

from Metrics import ndcg
from Utils.settings import Settings
from Utils.commons import prepare_folder

pd.set_option('display.max_columns', None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--task_name', type=str, required=True)
    parser.add_argument('--src_file_name', type=str, required=True)
    args = parser.parse_args()
    settings = Settings(args.db, args.task_name, args.src_file_name)

    dask.set_options(get=dask.multiprocessing.get)
    logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

    logging.info('Training: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):

        if args.draft:
            logging.info('Draft mode: ENABLED.')
            df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT + 'evaluation-*.csv',
                                         encoding=settings.ENCODING)
        else:
            logging.info('Draft mode: DISABLED.')
            df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'evaluation-*.csv',
                                         encoding=settings.ENCODING)

        X_evaluation = df_evaluation \
            .drop('best_answer', axis=1) \
            .drop('thread_id', axis=1) \
            .drop('post_id', axis=1) \
            .drop('Unnamed: 0', axis=1) \
            .drop('Unnamed: 0.1', axis=1) \
            .drop('index', axis=1).compute()
        y_evaluation = df_evaluation['best_answer'].compute()
        groups_evaluation = df_evaluation['thread_id'].compute()

        # print sanity checks
        logging.info('*******************************************************************************')
        logging.info('Sanity check for: df_evaluation')
        logging.info(pprint.pformat(df_evaluation.head(3)))
        logging.info('*******************************************************************************')


        clf = joblib.load(settings.OUTPUT_PATH_DIR_PICKLED + 'Pipeline_sklearn0.18.1.pkl')

        # predict the evaluation set and check it's score
        y_predictions = clf.predict(X_evaluation)

        # put all together
        df_predictions = pd.DataFrame.from_records({'y_true': y_evaluation,
                                                    'y_pred': y_predictions,
                                                    'thread_id': groups_evaluation,
                                                    'post_id': df_evaluation['post_id'].compute()})

        logging.info("Here's your predictions:" )
        logging.info(pprint.pformat(df_predictions.head()))

        def compute_metrics(df):
            # TODO check this
            return ndcg.ndcg_at_k(df['y_pred'], 1)

        # TODO sort predictions based on confidence, then enforce only 1 best answer

        # FIXME df_predictions['thread_id'] contains NaNs
        # FIXME dask.async.ValueError: cannot reindex from a duplicate axis
        ndcg_list = df_predictions.groupby('thread_id').apply(compute_metrics)

        # save predictions
        if args.draft:
            prepare_folder(settings.OUTPUT_PATH_DIR_PREDICTIONS_DRAFT)
            df_predictions.to_csv(settings.OUTPUT_PATH_DIR_PREDICTIONS_DRAFT + 'predictions.csv',
                                            encoding=settings.ENCODING)
        else:
            prepare_folder(settings.OUTPUT_PATH_DIR_PREDICTIONS)
            df_predictions.to_csv(settings.OUTPUT_PATH_DIR_PREDICTIONS + 'predictions.csv',
                                            encoding=settings.ENCODING)

        logging.info('nDCG@1: {}'.format(ndcg_list.mean()))

    logging.info('Training: completed.')

if __name__ == "__main__":
    main()
