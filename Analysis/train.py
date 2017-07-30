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
from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.svm import *
from sklearn.neighbors import *
from sklearn.tree import *
from sklearn.neural_network import *
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

        pipeline = Pipeline([('est', RandomForestClassifier())])  # RF is just a placeholder

        grid = [
            {
                'est': [MLPClassifier()],
                'est__hidden_layer_sizes': [(100,), (100, 100), (100, 100, 100)],
                'est__learning_rate': ['adaptive'],
                'est__random_state': [settings.RND_SEED],
            },
            {
                'est': [AdaBoostClassifier()],
                'est__base_estimator': [DecisionTreeClassifier(),
                                        RandomForestClassifier()],
                'est__n_estimators': [10, 100, 500],
                'est__learning_rate': [1, 2, 0.1],
                'est__random_state': [settings.RND_SEED],
            },
            {
                'est': [RandomForestClassifier()],
                'est__n_estimators': [10, 100, 500],
                'est__criterion': ['gini', 'entropy'],
                'est__max_features': ['auto', None, 'log2'],
                'est__max_depth': [None, 10],
                'est__min_samples_split': [2],
                'est__min_samples_leaf': [1],
                'est__min_weight_fraction_leaf': [0],
                'est__max_leaf_nodes': [None],
                'est__min_impurity_split': [1e-7],
                'est__bootstrap': [True, False],
                'est__oob_score': [False],
                'est__random_state': [settings.RND_SEED],
                'est__warm_start': [False],
                'est__verbose': [0],
                'est__n_jobs': [-1],
                'est__class_weight': [None,
                                      'balanced',
                                      {0: 1.0, 1: 10.0},
                                      {0: 1.0, 1: 2.0},
                                      ],
            },
            {
                'est': [LinearRegression()],
                'est__fit_intercept': [False, True],
                'est__normalize': [False, True],
                'est__copy_X': [True],
                'est__n_jobs': [-1],
            },
            {
                'est': [SVC()],
                'est__C': [0.1, 1, 10, 100],
                'est__kernel': ['linear', 'poly', 'rbf'],
                'est__degree': [2, 3, 5, 10],
                'est__probability': [True],
                'est__class_weight': [None,
                                      'balanced',
                                      {0: 1.0, 1: 10.0},
                                      {0: 1.0, 1: 2.0},
                                      ],
                'est__max_iter': [10000],
                'est__cache_size': [30000],
                'est__random_state': [settings.RND_SEED],
            },
            {
                'est': [KNeighborsClassifier()],
                'est__n_neighbors': [2, 5, 7, 10, 20, 30, 100],
                'est__weights': ['uniform', 'distance'],
                'est__algorithm': ['kd_tree', 'auto'],
                'est__leaf_size': [30, 5],
                'est__n_jobs': [-1],
            }
        ]

        for params in grid:
            est_name = params['est'][0].__class__.__name__
            logging.info('Training: {}'.format(est_name))

            ### double check the folds nr!
            cv_folds_nr = 10
            splitter = GroupShuffleSplit(n_splits=cv_folds_nr,
                                         train_size=settings.TRAIN_SIZE,
                                         random_state=settings.RND_SEED)
            split_cv = splitter.split(X_development, groups=groups_development)

            ### dask's GridSearchCV
            cv = dask_searchcv.GridSearchCV(pipeline,
                                            cv=split_cv,
                                            param_grid=params,
                                            scheduler='multiprocessing',
                                            refit=True,
                                            n_jobs=-1)

            # select the best model
            logging.info("Training started...")
            cv.fit(X_development, y_development, groups=groups_development)
            logging.info("Training finished")

            # save results in CSV + pickled models
            prepare_folder(settings.OUTPUT_PATH_DIR_RESULTS)
            pd.DataFrame().from_dict(cv.cv_results_).to_csv(settings.OUTPUT_PATH_DIR_RESULTS +
                                                            'GridSearchCV_results_{}.csv'.format(est_name),
                                                            encoding=settings.ENCODING)
            # Pickle the best estimator!
            prepare_folder(settings.OUTPUT_PATH_DIR_PICKLED)
            joblib.dump(cv.best_estimator_,
                        settings.OUTPUT_PATH_DIR_PICKLED +
                        '{}_sklearn{}.pkl'.format(est_name, sklearn.__version__), compress=True)

    logging.info('Training: completed.')

if __name__ == "__main__":
    main()
