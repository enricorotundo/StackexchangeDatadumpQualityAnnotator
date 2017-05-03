# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.preprocess_binaryBestAnswer

This script reads a feature matrix and pre-process it.
Output datapoints are indexed by thread_id.
"""

import logging

import numpy as np
import dask.multiprocessing
from dask.diagnostics import ProgressBar
import dask.dataframe as ddf
from Utils import settings_binaryBestAnswer as settings
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import Pipeline

dask.set_options(get=dask.multiprocessing.get)
logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

def main():
    logging.info('Pre-processing: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):
        df_training = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding=settings.ENCODING)
        df_testing = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding=settings.ENCODING)

        # TODO print some data, use "bokeh.io save plot"

        # TODO pre-processing: scaling
        # http://www.faqs.org/faqs/ai-faq/neural-nets/part2/section-16.html

        cols = []
        for col in df_training.columns:
            if col not in ['best_answer', 'thread_id', 'index']:
                cols.append(col)

        mapper = DataFrameMapper([
            (cols, StandardScaler(copy=False)),
            (['best_answer'], None),
            (['thread_id'], None),
            (['index'], None),
        ])

        dataset_training = mapper.fit_transform(df_training.compute())
        columns = [col for list in [tuple[0] for tuple in mapper.features] for col in list]

        df_training = ddf.from_array(dataset_training, columns=columns)
        df_training = df_training.repartition(npartitions=settings.N_PARTITIONS)

        # TODO do the same as above but on testing_set

        # TODO check for collinearity
        # http://onlinelibrary.wiley.com/doi/10.1890/08-0879.1/abstract

        # TODO others?

    logging.info('Pre-processing: completed.')

if __name__ == "__main__":
    main()