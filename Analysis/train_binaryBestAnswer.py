# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.train_binaryBestAnswer

Train a model on the development set (used in cross-validation).
Evaluate over the evaluation set (unseen, left-out).
"""

import logging
import argparse
import pprint

import dask
import dask.multiprocessing
import dask.dataframe as ddf
import pandas as pd

import dask_searchcv
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
from dask.diagnostics import ProgressBar

from Metrics import ndcg
from Utils import settings_binaryBestAnswer as settings
from Utils.commons import prepare_folder

dask.set_options(get=dask.multiprocessing.get)
logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    args = parser.parse_args()

    logging.info('Training: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):

        if args.draft:
            df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT + 'development-*.csv',
                                          encoding=settings.ENCODING)
            df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT + 'evaluation-*.csv',
                                         encoding=settings.ENCODING)
        else:
            df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'development-*.csv',
                                          encoding=settings.ENCODING)
            df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'evaluation-*.csv',
                                         encoding=settings.ENCODING)

        logging.info(pprint.pprint(sorted(df_development.columns)))

        X_development = df_development \
            .drop('best_answer', axis=1) \
            .drop('thread_id', axis=1) \
            .drop('post_id', axis=1) \
            .drop('Unnamed: 0', axis=1) \
            .drop('Unnamed: 0.1', axis=1) \
            .drop('index', axis=1).compute()
        y_development = df_development['best_answer'].compute()
        groups_development = df_development['thread_id'].compute()

        X_evaluation = df_evaluation \
            .drop('best_answer', axis=1) \
            .drop('thread_id', axis=1) \
            .drop('post_id', axis=1) \
            .drop('Unnamed: 0', axis=1) \
            .drop('Unnamed: 0.1', axis=1) \
            .drop('index', axis=1).compute()
        y_evaluation = df_evaluation['best_answer'].compute()

        clf = RandomForestClassifier()
        pipeline = Pipeline([('random_forest', clf)])

        parameters = {'random_forest__n_estimators': [50, 100, 300],
                      'random_forest__criterion': ['gini', 'entropy'],
                      'random_forest__max_features': ['auto'],
                      'random_forest__max_depth': [None],
                      'random_forest__min_samples_split': [2],
                      'random_forest__min_samples_leaf': [1],
                      'random_forest__min_weight_fraction_leaf': [0],
                      'random_forest__max_leaf_nodes': [None],
                      'random_forest__min_impurity_split': [1e-7],
                      'random_forest__bootstrap': [True],
                      'random_forest__oob_score': [False],
                      'random_forest__random_state': [settings.RND_SEED],
                      'random_forest__warm_start': [False],
                      'random_forest__verbose': [0],
                      'random_forest__n_jobs': [-1]
                      }

        # make sure to pass same params as in split_binaryBestAnswer
        splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=settings.RND_SEED)
        split_cv = splitter.split(X_development, groups=df_development['thread_id'])

        # dask's GridSearchCV
        cv = dask_searchcv.GridSearchCV(pipeline, cv=split_cv, param_grid=parameters, scheduler='multiprocessing')
        # scikit's GridSearchCV (better use the one above)
        ##cv = GridSearchCV(pipeline, cv=split_cv, param_grid=parameters)

        # select the best model
        cv.fit(X_development, y_development, groups=groups_development)

        # predict the evaluation set and check it's score
        y_predictions = ddf.from_array(cv.predict(X_evaluation))

        # align divisions
        groups = df_development['thread_id']
        y_evaluation.divisions = y_predictions.divisions
        groups.divisions = y_predictions.divisions

        # put all together
        df_predictions = dask.dataframe.concat([y_evaluation, y_predictions, groups], axis=1)
        df_predictions.columns = ['y_true', 'y_pred', 'thread_id']

        # TODO print more predictions

        def compute_metrics(df):
            # TODO check this
            return ndcg.ndcg_at_k(df['y_pred'], 1)

        # FIXME df_predictions['thread_id'] contains NaNs
        # FIXME dask.async.ValueError: cannot reindex from a duplicate axis
        ndcg_list = df_predictions.groupby('thread_id').apply(compute_metrics, meta=('x', 'f8')).compute()

        # save predictions
        if args.draft:
            prepare_folder(settings.OUTPUT_PATH_DIR_PREDICTIONS_DRAFT)
            df_predictions.compute().to_csv(settings.OUTPUT_PATH_DIR_PREDICTIONS_DRAFT + 'predictions.csv',
                                            encoding=settings.ENCODING)
        else:
            prepare_folder(settings.OUTPUT_PATH_DIR_PREDICTIONS)
            df_predictions.compute().to_csv(settings.OUTPUT_PATH_DIR_PREDICTIONS + 'predictions.csv',
                                            encoding=settings.ENCODING)

        logging.info('nDCG@1: {}'.format(ndcg_list.mean()))

    logging.info('Training: completed.')

if __name__ == "__main__":
    main()
