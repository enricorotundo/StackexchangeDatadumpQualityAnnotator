# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.split_binaryBestAnswer

This script reads a feature matrix and splits it into a development and evaluation set.

http://scikit-learn.org/stable/modules/grid_search.html#model-selection-development-and-evaluation
"""

import glob
import os
import logging

import dask.dataframe as ddf
import dask.multiprocessing
from dask import delayed
from sklearn.model_selection import GroupShuffleSplit

from Analysis.Utils.delayed import selector
from Utils import settings_binaryBestAnswer as settings

logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)
dask.set_options(get=dask.multiprocessing.get)


def main():
    logging.info('Dataset splitting: started.')

    df = ddf.read_csv(settings.OUTPUT_PATH_DIR + '*.csv', encoding=settings.ENCODING)

    # sequence of randomized partitions in which a subset of groups are held out for each split
    splitter = GroupShuffleSplit(n_splits=1, train_size=settings.TRAIN_SIZE, random_state=settings.RND_SEED)

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
    df_training = df_training.repartition(npartitions=settings.N_PARTITIONS)
    df_testing = ddf.from_delayed(delayed_evaluation, meta=df)
    df_testing = df_testing.repartition(npartitions=settings.N_PARTITIONS)

    # create output directory
    if not os.path.exists(settings.OUTPUT_PATH_DIR_SPLITTED):
        logging.info('Creating output directory in {}.'.format(settings.OUTPUT_PATH_DIR_SPLITTED))
        os.makedirs(settings.OUTPUT_PATH_DIR_SPLITTED)

    # clear output folder first
    filelist = glob.glob(settings.OUTPUT_PATH_DIR_SPLITTED + "*.csv")
    for f in filelist:
        logging.info('Clearing output directory: {}.'.format(f))
        os.remove(f)

    df_training.to_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding=settings.ENCODING)
    df_testing.to_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding=settings.ENCODING)

    logging.info('Dataset splitting: completed.')

if __name__ == "__main__":
    main()
