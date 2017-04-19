# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.train_binaryBestAnswer

This script reads a train/test set, train models and run evaluation
"""


import dask

dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42




def main():
    """
    clf = sklearn.ensemble.RandomForestClassifier()

    pipelines_steps = [('random_forest', clf)]
    pipeline = sklearn.pipeline.Pipeline(pipelines_steps)
    parameters = dict(random_forest__n_estimators=[50, 100])
    cv = GridSearchCV(pipeline, cv=5, param_grid=parameters)
    cv.fit(X_train, y_train)
    y_predictions = cv.predict(X_test)
    report = sklearn.metrics.classification_report(y_test, y_pred)
    print report
    """


if __name__ == "__main__":
    main()