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
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn_pandas import DataFrameMapper
from sklearn.pipeline import Pipeline

from Utils import settings_binaryBestAnswer as settings
from Utils.commons import prepare_folder

dask.set_options(get=dask.multiprocessing.get)
logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

def main():
    logging.info('Pre-processing: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):
        df_development = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'development-*.csv', encoding=settings.ENCODING)
        df_evaluation = ddf.read_csv(settings.OUTPUT_PATH_DIR_SPLITTED + 'evaluation-*.csv', encoding=settings.ENCODING)

        # get features columns names
        cols = []
        for col in df_development.columns:
            if col not in ['best_answer', 'thread_id', 'index']:
                cols.append(col)

        # TODO print some data, use "bokeh.io save plot"

        # pre-processing: scaling (http://www.faqs.org/faqs/ai-faq/neural-nets/part2/section-16.html)
        # TODO consider sklearn.preprocessing.RobustScaler for outliers!!!!!

        mapper = DataFrameMapper([
            (cols, StandardScaler(copy=False)),
            (['best_answer'], None),
            (['thread_id'], None),
            (['index'], None),
        ])


        prepare_folder(settings.OUTPUT_PATH_DIR_PREPROC)

        # process development data
        dataset_development = mapper.fit_transform(df_development.compute())
        columns = [col for list in [tuple[0] for tuple in mapper.features] for col in list]
        df_development = ddf.from_array(dataset_development, columns=columns)
        df_development.to_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'development-*.csv', encoding=settings.ENCODING)

        # process evaluation data
        dataset_evaluation = mapper.transform(df_evaluation.compute())
        df_evaluation = ddf.from_array(dataset_evaluation, columns=columns)
        df_evaluation.to_csv(settings.OUTPUT_PATH_DIR_PREPROC + 'evaluation-*.csv', encoding=settings.ENCODING)


        # TODO plot boxplot for columns

        # TODO check for collinearity
        # http://onlinelibrary.wiley.com/doi/10.1890/08-0879.1/abstract

        # TODO others?

    logging.info('Pre-processing: completed.')

if __name__ == "__main__":
    main()