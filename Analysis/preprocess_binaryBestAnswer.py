# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.preprocess_binaryBestAnswer

This script reads a feature matrix and pre-process it.
Output datapoints are indexed by thread_id.
"""

import logging
import argparse

import dask.multiprocessing
from dask.diagnostics import ProgressBar
import dask.dataframe as ddf
from sklearn.preprocessing import StandardScaler
from sklearn_pandas import DataFrameMapper

from Utils import settings_binaryBestAnswer as settings
from Utils.commons import prepare_folder

dask.set_options(get=dask.multiprocessing.get)
logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--plot', action='store_true')
    args = parser.parse_args()

    logging.info('Pre-processing: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):
        if args.draft:
            logging.info('Draft mode: Enabled... Opening {}'.format(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT + '*.csv'))
            df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT + 'development-*.csv',
                                          encoding=settings.ENCODING)
            df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED_DRAFT + 'evaluation-*.csv',
                                         encoding=settings.ENCODING)
        else:
            logging.info('Draft mode: Disabled... Opening {}'.format(settings.OUTPUT_PATH_DIR_SPLITTED + '*.csv'))
            df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv',
                                          encoding=settings.ENCODING)
            df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv',
                                         encoding=settings.ENCODING)


        meta_cols = ['best_answer', 'thread_id', 'index', 'post_id']
        # get features columns names
        cols = []
        for col in df_development.columns:
            if col not in meta_cols:
                cols.append(col)

        logging.info('Meta columns: {}'.format(meta_cols))
        logging.info('IV cols: {}'.format(sorted(cols)))

        # TODO print some data, use "bokeh.io save plot"

        # pre-processing: scaling (http://www.faqs.org/faqs/ai-faq/neural-nets/part2/section-16.html)
        # TODO consider sklearn.preprocessing.RobustScaler for outliers!!!!!

        mapper = DataFrameMapper([
            (cols, StandardScaler(copy=False)),
            (meta_cols, None),
        ])

        # process development data
        dataset_development = mapper.fit_transform(df_development.compute())
        columns = [col for list in [tuple[0] for tuple in mapper.features] for col in list]
        df_development = ddf.from_array(dataset_development, columns=columns)

        # process evaluation data
        dataset_evaluation = mapper.transform(df_evaluation.compute())
        df_evaluation = ddf.from_array(dataset_evaluation, columns=columns)

        if args.draft:
            prepare_folder(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT)
            logging.info('Draft mode: Enabled... Saving in {}'.format(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT))
            df_development.to_csv(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT + 'development-*.csv',
                                  encoding=settings.ENCODING)
            df_evaluation.to_csv(settings.OUTPUT_PATH_DIR_PREPROC_DRAFT + 'evaluation-*.csv',
                                 encoding=settings.ENCODING)
        else:
            prepare_folder(settings.OUTPUT_PATH_DIR_PREPROC)
            logging.info('Draft mode: Disabled... Saving in {}'.format(settings.OUTPUT_PATH_DIR_PREPROC))
            df_development.to_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'development-*.csv',
                                  encoding=settings.ENCODING)
            df_evaluation.to_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'evaluation-*.csv',
                                 encoding=settings.ENCODING)

        if args.plot:
            logging.info('Plot mode: Enabled. It might take a while.')
            # TODO plot boxplot for columns
        else:
            logging.info('Plot mode: Disabled... This should save you time.')

        # TODO check for collinearity
        # http://onlinelibrary.wiley.com/doi/10.1890/08-0879.1/abstract

        # TODO others?

    logging.info('Pre-processing: completed.')

if __name__ == "__main__":
    main()