# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.split_binaryBestAnswer

This script reads a feature matrix and splits it into training and test set.
 
Note: have a look at the following questions:
http://stackoverflow.com/questions/43364921/how-to-select-data-with-list-of-indexes-from-a-partitioned-df-non-unique-indexe
https://github.com/dask/dask/issues/2203
"""

import dask.dataframe as ddf
from dask import delayed
import dask
from sklearn.model_selection import GroupShuffleSplit

dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42



@delayed
def selector(df, i):
    """Called from delayed objects"""
    return df.loc[[i]]  # needs double brackets so always return a dask.DataFrame


def main():
    df = ddf.read_csv(OUTPUT_PATH_DIR + '*.part.csv', encoding='utf-8')


    # TODO: pre-processing: normalization

    # TODO: pre-processing: scaling


    # split training/testing set
    splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=RND_SEED)
    # indexes are relative to the related partition
    delayed_train = []
    delayed_test = []
    for partition_index in xrange(df.npartitions):

        X = df.get_partition(partition_index)\
                .drop('best_answer', axis=1)\
                .drop('thread_id', axis=1)

        # splitting-train-test: use 'thread_id' as groups labels
        groups = df.get_partition(partition_index)['thread_id']
        # with n_splits=1 split returns only one generator, so .next()
        train_indexes, test_indexes = splitter.split(X, groups=groups).next()

        delayed_train.extend([delayed(selector)(df.get_partition(partition_index), i) for i in train_indexes])
        delayed_test.extend([delayed(selector)(df.get_partition(partition_index), i) for i in test_indexes])

    df_training = ddf.from_delayed(delayed_train, meta=df)
    df_training = df_training.repartition(npartitions=4)

    df_testing = ddf.from_delayed(delayed_test, meta=df)
    df_testing = df_testing.repartition(npartitions=4)


    df_training.to_csv(OUTPUT_PATH_DIR_SPLITTED + 'train-*.csv', encoding='utf-8')
    df_testing.to_csv(OUTPUT_PATH_DIR_SPLITTED + 'test-*.csv', encoding='utf-8')





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