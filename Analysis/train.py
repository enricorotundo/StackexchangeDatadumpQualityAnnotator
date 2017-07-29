# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.train

Train a model on the development set (used in cross-validation).
"""

import logging
import argparse
import pprint

import dask
import dask.multiprocessing
import dask.dataframe as ddf
import pandas as pd
import sklearn

import dask_searchcv
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
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
            df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT + 'development-*.csv',
                                          encoding=settings.ENCODING)
        else:
            logging.info('Draft mode: DISABLED.')
            df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'development-*.csv',
                                          encoding=settings.ENCODING)

        X_development = df_development \
            .drop('best_answer', axis=1) \
            .drop('thread_id', axis=1) \
            .drop('post_id', axis=1) \
            .drop('Unnamed: 0', axis=1) \
            .drop('Unnamed: 0.1', axis=1) \
            .drop('index', axis=1).compute()
        y_development = df_development['best_answer'].compute()
        groups_development = df_development['thread_id'].compute()

        # print sanity checks
        logging.info('*******************************************************************************')
        logging.info('Sanity check for: df_development')
        logging.info(pprint.pformat(df_development.head(3)))
        logging.info('*******************************************************************************')
        logging.info('Make sure there are only IV columns:')
        logging.info(pprint.pformat(pprint.pformat(sorted(X_development.columns))))
        logging.info('*******************************************************************************')

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
        logging.info('Parameters for {}:'.format(clf.__class__.__name__))
        logging.info(pprint.pformat(parameters))

        cv_folds_nr = 1
        splitter = GroupShuffleSplit(n_splits=cv_folds_nr, train_size=settings.TRAIN_SIZE, random_state=settings.RND_SEED)
        split_cv = splitter.split(X_development, groups=groups_development)

        ### dask's GridSearchCV
        cv = dask_searchcv.GridSearchCV(pipeline,
                                        cv=split_cv,
                                        param_grid=parameters,
                                        scheduler='multiprocessing',
                                        refit=True,
                                        n_jobs=-1)
        ### scikit's GridSearchCV (better use the one above)
        #optimal_estimator = sklearn.model_selection.GridSearchCV(pipeline, cv=split_cv, param_grid=parameters)

        # select the best model
        logging.info("Training started...")
        cv.fit(X_development, y_development, groups=groups_development)
        logging.info("Training finished")

        logging.info(pprint.pformat(cv.best_score_))
        logging.info(pprint.pformat(cv.best_params_))
        logging.info(pprint.pformat(cv.cv_results_))


        # Pickle the best estimator!
        joblib.dump(cv.best_estimator_,
                    'PickledModels/{}_sklearn{}.pkl'.format(clf.__class__.__name__, sklearn.__version__),
                    compress=True)


    logging.info('Training: completed.')

if __name__ == "__main__":
    main()
