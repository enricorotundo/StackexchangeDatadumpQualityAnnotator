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

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import make_scorer
from sklearn.preprocessing import add_dummy_feature

dask.set_options(get=dask.multiprocessing.get)

from Metrics import ndcg

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42


def score_func(data):
    #print data
    return 1

def scorer(estimator, X, y):
    """
    :param estimator: sklearn.pipeline.Pipeline
    :param X: pandas.core.frame.DataFrame
    :param y: pandas.core.series.Series
    :return: float
    """
    # prep data
    y_true = pd.DataFrame(y)
    y_true.columns = ['y_true']

    # let's predict! add_dummy_feature replaces the dropped thread_id column
    y_pred = pd.DataFrame(estimator.predict(X), index=y_true.index, columns=['y_pred'])
    #print y_pred.index
    #print y_pred.index

    #print groups

    # put together y_true, y_pred, thread_id
    ##y_df = pd.concat([y_true, y_pred, groups], axis=1)

    ##y_df.groupby('thread_id').apply(lambda data: score_func(data))

    print "****"
    return 1.0


def main():
    df_development = ddf.read_csv(OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding='utf-8')
    df_evaluation = ddf.read_csv(OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding='utf-8')

    X_development = df_development \
        .drop('thread_id', axis=1) \
        .drop('Unnamed: 0', axis=1) \
        .drop('Unnamed: 0.1', axis=1)
    y_development = df_development['best_answer']

    clf = RandomForestClassifier(verbose=0, n_jobs=-1, random_state=RND_SEED)
    pipeline = Pipeline([('random_forest', clf)])

    parameters = dict(random_forest__n_estimators=[1])
    splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=RND_SEED)
    split_cv = splitter.split(X_development, groups=df_development['thread_id'])

    # TODO passare a scorer un DataFrame con i thread_id della stessa dimensione di X_development !!!!!!!
    # TODO splittare qui e settare come global? dovrebbe funzionare
    dev_indexes, eval_indexes = splitter.split(df_development['thread_id'], groups=df_development['thread_id']).next()

    cv = dask_searchcv.GridSearchCV(pipeline, cv=split_cv, param_grid=parameters, scoring=scorer,
                                    scheduler='threading')

    # this selects the best model (in terms of NDCG?)
    cv.fit(X_development, y_development, groups=df_development['thread_id'])

    # predict the evaluation set and check it's score
    #y_predictions = cv.predict(X_evaluation)

if __name__ == "__main__":
    main()
