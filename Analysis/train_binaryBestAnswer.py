# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.train_binaryBestAnswer

Train a model on the development set (used in cross-validation).
Evaluate over the evaluation set (unseen, left-out).
"""

import pandas as pd
import numpy as np
import dask
import sklearn
import dask_searchcv
import dask.multiprocessing
import dask.dataframe as ddf

from dask import delayed
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import make_scorer
from sklearn.preprocessing import add_dummy_feature
from Analysis.Utils.delayed import selector
from sklearn.metrics import classification_report
from Metrics import ndcg

dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42

"""
# CUSTOM SCORER PART, TMP COMMENTED, WAITING FOR ANSWERS
def scorer(estimator, X, y):
    
    Performs and evaluation of estimator.
     
    :param estimator: sklearn.pipeline.Pipeline
    :param X: pandas.core.frame.DataFrame
    :param y: pandas.core.series.Series
    :return: float
    
    # prep data
    y_true = pd.DataFrame(y)
    y_true.columns = ['y_true']

    # let's predict!
    y_pred = pd.DataFrame(estimator.predict(X), index=y_true.index, columns=['y_pred'])

    print y_true.index
    print y_pred.index
    print df_groups.compute()

    # put together y_true, y_pred, thread_id
    #y_df = pd.concat([y_true, y_pred, df_groups_eval.compute()], axis=1)

    ##y_df.groupby('thread_id').apply(lambda data: score_func(data))


    print "*********************** \n\n\n"
    return 1.0
"""


def main():
    df_development = ddf.read_csv(OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding='utf-8')
    df_evaluation = ddf.read_csv(OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding='utf-8')


    X_development = df_development \
        .drop('best_answer', axis=1) \
        .drop('thread_id', axis=1) \
        .drop('Unnamed: 0', axis=1) \
        .drop('Unnamed: 0.1', axis=1)
    y_development = df_development['best_answer']

    X_evaluation = df_evaluation \
        .drop('best_answer', axis=1) \
        .drop('thread_id', axis=1) \
        .drop('Unnamed: 0', axis=1) \
        .drop('Unnamed: 0.1', axis=1)
    y_evaluation = df_evaluation['best_answer']

    clf = RandomForestClassifier(verbose=0, n_jobs=-1, random_state=RND_SEED)
    pipeline = Pipeline([('random_forest', clf)])
    parameters = dict(random_forest__n_estimators=[50, 100])


    """
    # CUSTOM SCORER PART, TMP COMMENTED, WAITING FOR ANSWERS
    
    dev_indexes, eval_indexes = splitter.split(df_development['thread_id'], groups=df_development['thread_id']).next()
    
    # build global groups dataframes, 1 for dev, 1 for eval
    delayed_dev_groups = [delayed(selector)(df_development['thread_id'], i) for i in dev_indexes]
    #delayed_eval_groups = [delayed(selector)(df_development[['thread_id']], i) for i in eval_indexes]
    global df_groups_dev
    #global df_groups_eval
    df_groups_dev = ddf.from_delayed(delayed_dev_groups, meta=df_development[['thread_id']])
    #df_groups_eval = ddf.from_delayed(delayed_eval_groups, meta=df_development[['thread_id']])
    
    cv = dask_searchcv.GridSearchCV(pipeline, cv=split_cv, param_grid=parameters, scoring=scorer,
                                    scheduler='threading')
    """

    # make sure to pass same params as in split_binaryBestAnswer
    splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=RND_SEED)
    split_cv = splitter.split(X_development, groups=df_development['thread_id'])

    cv = dask_searchcv.GridSearchCV(pipeline, cv=split_cv, param_grid=parameters, scheduler='multiprocessing')

    # select the best model
    cv.fit(X_development.compute(), y_development.compute(), groups=df_development['thread_id'].compute())

    # predict the evaluation set and check it's score
    y_predictions = ddf.from_array(cv.predict(X_evaluation))

    # align divisions
    groups = df_development['thread_id']
    y_evaluation.divisions = y_predictions.divisions
    groups.divisions = y_predictions.divisions

    # put all together
    df_predictions = dask.dataframe.concat([y_evaluation, y_predictions, groups], axis=1)
    df_predictions.columns = ['y_true', 'y_pred', 'thread_id']

    def compute_metrics(df):
        return ndcg.ndcg_at_k(df['y_pred'], 1)

    ndcg_list = df_predictions.groupby('thread_id').apply(compute_metrics, meta=('x', 'f8')).compute()

    print 'nDCG@1: {}'.format(ndcg_list.mean())

if __name__ == "__main__":
    main()
