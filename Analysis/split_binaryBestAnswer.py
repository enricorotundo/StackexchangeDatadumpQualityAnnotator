# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.split_binaryBestAnswer

This script reads a feature matrix and splits it into a development and evaluation set.
Expects datapoints indexed by thread_id, although that's not the case for the output. 

http://scikit-learn.org/stable/modules/grid_search.html#model-selection-development-and-evaluation
"""

import logging
import argparse

import dask.dataframe as ddf
import dask.multiprocessing
from dask import delayed
from sklearn.model_selection import GroupShuffleSplit
from dask.diagnostics import ProgressBar

from Analysis.Utils.delayed import selector
from Utils import settings_binaryBestAnswer as settings
from Utils.commons import prepare_folder

logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)
dask.set_options(get=dask.multiprocessing.get)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--n_partitions', type=int)
    args = parser.parse_args()

    logging.info('Dataset splitting: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):

        if args.draft:
            logging.info('Draft mode: Enabled... Opening {}'.format(settings.OUTPUT_PATH_DIR_DRAFT + '*.csv'))
            df = ddf.read_csv(settings.OUTPUT_PATH_DIR_DRAFT + '*.csv', encoding=settings.ENCODING)
        else:
            logging.info('Draft mode: Disabled... Opening {}'.format(settings.OUTPUT_PATH_DIR + '*.csv'))
            df = ddf.read_csv(settings.OUTPUT_PATH_DIR + '*.csv', encoding=settings.ENCODING)

        # sequence of randomized partitions in which a subset of groups are held out for each split
        splitter = GroupShuffleSplit(n_splits=1, train_size=settings.TRAIN_SIZE, random_state=settings.RND_SEED)

        # delayed rows (dask.DataFrame) of the final DataFrame
        delayed_development = []
        delayed_evaluation = []

        # assumes thread_id are correctly split over partitions (assured by feats_extract step!)
        for partition_index in xrange(df.npartitions):
            logging.info('Processing partition {}/{}'.format(partition_index+1, df.npartitions))
            df_partition = df.get_partition(partition_index)
            df_partition = df_partition.reset_index()  # necessary as thread_id is index
            groups = df.get_partition(partition_index)['thread_id']  # 'thread_id' as groups
            # with n_splits=1, split returns only one generator, so .next()
            indexes_development, indexes_evaluation = splitter.split(df_partition, groups=groups).next()
            # create delayed objects lists
            delayed_development.extend([delayed(selector)(df_partition, i) for i in indexes_development])
            delayed_evaluation.extend([delayed(selector)(df_partition, i) for i in indexes_evaluation])

        # from delayed -> DataFrame
        df_training = ddf.from_delayed(delayed_development, meta=df)
        df_training = df_training.repartition(npartitions=args.n_partitions)
        df_testing = ddf.from_delayed(delayed_evaluation, meta=df)
        df_testing = df_testing.repartition(npartitions=args.n_partitions)

        if args.draft:
            prepare_folder(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT)
            logging.info('Draft mode: Enabled... Saving in {}'.format(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT))
            df_training.to_csv(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT + 'development-*.csv', encoding=settings.ENCODING)
            df_testing.to_csv(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT + 'evaluation-*.csv', encoding=settings.ENCODING)
        else:
            prepare_folder(settings.OUTPUT_PATH_DIR_SPLITTED)
            logging.info('Draft mode: Disabled... Saving in {}'.format(settings.OUTPUT_PATH_DIR_SPLITTED))
            df_training.to_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding=settings.ENCODING)
            df_testing.to_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding=settings.ENCODING)

    logging.info('Dataset splitting: completed.')

if __name__ == "__main__":
    main()
