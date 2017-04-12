# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.train_binaryBestAnswer

This script reads the feature matrix, splits it into training and test set
 
Note: inefficient, waiting for the following questions:
http://stackoverflow.com/questions/43364921/how-to-select-data-with-list-of-indexes-from-a-partitioned-df-non-unique-indexe
https://github.com/dask/dask/issues/2203
"""

import numpy as np
import dask.dataframe as ddf
import dask
from sklearn.model_selection import GroupShuffleSplit
import sklearn.pipeline
from sklearn.model_selection import GridSearchCV

dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42



def main():
    df = ddf.read_csv(OUTPUT_PATH_DIR + '*.part.csv', encoding='utf-8')

    # TODO: pre-processing: normalization

    # TODO: pre-processing: scaling

    splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=RND_SEED)
    # indexes are relative to the related partition
    train_indexes_list = []
    test_indexes_list = []
    for partition_index in xrange(df.npartitions):

        X = df.get_partition(partition_index)\
                .drop('best_answer', axis=1)\
                .drop('thread_id', axis=1)

        # splitting-train-test: use 'thread_id' as groups labels
        groups = df.get_partition(partition_index)['thread_id']
        train_indexes, test_indexes = splitter.split(X, groups=groups).next()
        train_indexes_list.append(train_indexes)
        test_indexes_list.append(test_indexes)


    # compute offsets for train_indexes and test_indexes
    partitions_offsets = []
    for i in xrange(df.npartitions):
        if i == 0:
            partitions_offsets.append(0)
        else:
            partitions_offsets.append(len(df.get_partition(i)))

    # training set indexes
    incr_offset = 0
    train_indexes_list_offsetted = []
    for index, offset in enumerate(partitions_offsets):
        train_indexes_list_offsetted.append(train_indexes_list[index] + offset + incr_offset)
        incr_offset = incr_offset + offset
    train_indexes_offsetted_flat = [index for index_list in train_indexes_list_offsetted for index in index_list]

    # test set indexes
    incr_offset = 0
    test_indexes_list_offsetted = []
    for index, offset in enumerate(partitions_offsets):
        test_indexes_list_offsetted.append(test_indexes_list[index] + offset + incr_offset)
        incr_offset = incr_offset + offset
    test_indexes_offsetted_flat = [index for index_list in test_indexes_list_offsetted for index in index_list]

    print len(train_indexes_offsetted_flat)
    print len(test_indexes_offsetted_flat)

    """
    df_training = ddf.concat([df.loc[i] for i in train_indexes_offsetted_flat])
    df_test = ddf.concat([df.loc[i] for i in test_indexes_offsetted_flat])
    print df_training.size.compute()
    print df_test.size.compute()
    """


    """
    
    13:30 min
    
    TODO:
    alternative, instead of creating new df, just create a column say if it's training_set 
    0/1 and attach it to the original df
    """





    """
    for partition_index, index_list in enumerate(train_indexes_list):
        dask.concat([df.get_partition(partition_index).loc[index] for index in index_list])
    """



    """
    X_train = X.iloc[train_indexes]
    y_train = y.iloc[train_indexes]
    X_test = X.iloc[test_indexes]
    y_test = y.iloc[test_indexes]
    """

    #print df.head()

    #print type(train_indexes)
    #print df.loc[0].compute()
    #print df.loc[train_indexes].compute()


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