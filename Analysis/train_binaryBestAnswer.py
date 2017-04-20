# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.train_binaryBestAnswer

Train a model on the development set (used in cross-validation).
Evaluate over the evaluation set (unseen, left-out).
"""


import dask
import dask.multiprocessing
import dask.dataframe as ddf
import sklearn
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import make_scorer

dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42


def scorer(estimator, X, y):
    """Should implement nDCG"""
    return 1


def main():
    df_development = ddf.read_csv(OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding='utf-8')
    df_evaluation = ddf.read_csv(OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding='utf-8')

    global threads
    threads = df_development['thread_id']

    X_development = df_development\
        .drop('best_answer', axis=1) \
        .drop('thread_id', axis=1) \
        .drop('Unnamed: 0', axis=1) \
        .drop('Unnamed: 0.1', axis=1).compute()
    y_development = df_development['best_answer'].compute()

    X_evaluation = df_evaluation\
        .drop('best_answer', axis=1) \
        .drop('thread_id', axis=1) \
        .drop('Unnamed: 0', axis=1) \
        .drop('Unnamed: 0.1', axis=1).compute()
    y_evaluation = df_evaluation['best_answer'].compute()

    # TODO specify a LETOR evaluation scoring function

    clf = RandomForestClassifier(verbose=0, n_jobs=-1)
    pipeline = Pipeline([('random_forest', clf)])

    parameters = dict(random_forest__n_estimators=[50, 100])
    splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=RND_SEED) \
        .split(X_development, groups=df_development['thread_id'])

    cv = GridSearchCV(pipeline,
                      cv=splitter,
                      param_grid=parameters,
                      scoring=scorer)

    cv.fit(X_development, y_development)
    y_predictions = cv.predict(X_evaluation)

    #print cv.best_score_


if __name__ == "__main__":
    main()
