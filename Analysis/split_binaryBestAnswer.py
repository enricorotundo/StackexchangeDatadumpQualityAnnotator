# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.split_binaryBestAnswer

This script reads a feature matrix and splits it into a development and evaluation set.

http://scikit-learn.org/stable/modules/grid_search.html#model-selection-development-and-evaluation
"""

import dask.dataframe as ddf
import dask.multiprocessing
from dask import delayed
from sklearn.model_selection import GroupShuffleSplit

from Analysis.Utils.delayed import selector

dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42


def main():
    df = ddf.read_csv(OUTPUT_PATH_DIR + '*.part.csv', encoding='utf-8')

    # sequence of randomized partitions in which a subset of groups are held out for each split
    splitter = GroupShuffleSplit(n_splits=1, train_size=0.7, random_state=RND_SEED)

    # delayed rows (dask.DataFrame) of the final DataFrame
    delayed_development = []
    delayed_evaluation = []

    # assumes thread_id are correctly split over partitions
    for partition_index in xrange(df.npartitions):
        df_partition = df.get_partition(partition_index)
        # 'thread_id' as groups
        groups = df.get_partition(partition_index)['thread_id']
        # with n_splits=1, split returns only one generator, so .next()
        indexes_development, indexes_evaluation = splitter.split(df_partition, groups=groups).next()
        # create delayed objects lists
        delayed_development.extend([delayed(selector)(df_partition, i) for i in indexes_development])
        delayed_evaluation.extend([delayed(selector)(df_partition, i) for i in indexes_evaluation])

    # from delayed -> DataFrame
    df_training = ddf.from_delayed(delayed_development, meta=df)
    df_training = df_training.repartition(npartitions=4)
    df_testing = ddf.from_delayed(delayed_evaluation, meta=df)
    df_testing = df_testing.repartition(npartitions=4)

    df_training.to_csv(OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding='utf-8')
    df_testing.to_csv(OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding='utf-8')


if __name__ == "__main__":
    main()
