# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.test

Evaluate over the evaluation set (unseen, left-out).
"""

import logging
import argparse
import pprint
import glob

import dask
import dask.multiprocessing
import dask.dataframe as ddf
import pandas as pd
import numpy as np

from dask.diagnostics import ProgressBar
from sklearn.externals import joblib

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

    logging.info('Testing: started.')

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

        for file_path in glob.glob(settings.OUTPUT_PATH_DIR_PICKLED + '*.pkl'):
            clf = joblib.load(file_path)
            model_name = clf.steps[0][1].__class__.__name__
            logging.info('Estimator name: {}'.format(model_name))

            # predict on the test set
            y_predictions = clf.predict(X_evaluation)

            try:
                y_proba = clf.predict_proba(X_evaluation)
            except:
                y_proba = []

            # put all together
            if len(y_proba) > 0:
                df_predictions = pd.DataFrame.from_records({'y_true': y_evaluation,
                                                        'y_pred': y_predictions,
                                                        'thread_id': groups_evaluation,
                                                        'post_id': df_evaluation['post_id'].compute(),
                                                        'pred_proba_class0': [prob[0] for prob in y_proba],
                                                        'pred_proba_class1': [prob[1] for prob in y_proba],
                                                        'rnd_pred': np.random.randint(2, size=len(y_predictions))
                                                        })\
                                .sort_values('thread_id')
            else:
                df_predictions = pd.DataFrame.from_records({'y_true': y_evaluation,
                                                            'y_pred': y_predictions,
                                                            'thread_id': groups_evaluation,
                                                            'post_id': df_evaluation['post_id'].compute(),
                                                            'pred_proba_class0': [np.NaN] * len(y_predictions),
                                                            'pred_proba_class1': [np.NaN] * len(y_predictions),
                                                            'rnd_pred': np.random.randint(2, size=len(y_predictions))
                                                            }) \
                    .sort_values('thread_id')

            # this makes sense if there are at least 2 answers per thread
            def feats_post_processing(df):
                # take the answer with highest probability of being a best-answer
                row_max_pred = df[df['pred_proba_class1'] == df['pred_proba_class1'].max()]
                # elect that as best-answer
                row_max_pred['y_pred_post'] = 1.0
                # all the others are not best answers
                other_rows = df[df['pred_proba_class1'] != df['pred_proba_class1'].max()]
                # set them as not best-ones!
                other_rows['y_pred_post'] = 0.0

                return pd.concat([row_max_pred, other_rows])

            # post-processing: make sure 1 and only 1 predicted best-answer per thread!
            #if len(y_proba) > 0:
            df_predictions = df_predictions.groupby('thread_id').apply(feats_post_processing)

            # save predictions
            prepare_folder(settings.OUTPUT_PATH_DIR_PREDICTIONS, clear=False)
            df_predictions.to_csv(settings.OUTPUT_PATH_DIR_PREDICTIONS + '{}_predictions.csv'.format(model_name),
                                  encoding=settings.ENCODING)

            logging.info("Here's your predictions:")
            logging.info(pprint.pformat(df_predictions.head()))


    logging.info('Testing: completed.')

if __name__ == "__main__":
    main()
