# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.preprocess

This script reads a feature matrix and pre-process it.
Output datapoints are indexed by thread_id.
"""

import logging
import argparse

import dask.multiprocessing
from dask.diagnostics import ProgressBar
import dask.dataframe as ddf
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn_pandas import DataFrameMapper
from bokeh.charts import Histogram, BoxPlot, output_file, show, save
import pandas as pd

from Utils.settings import Settings
from Utils.commons import prepare_folder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true')
    parser.add_argument('--plot', action='store_true')
    parser.add_argument('--scaler', default='standard', choices=['standard', 'robust'])
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--task_name', type=str, required=True)
    parser.add_argument('--src_file_name', type=str, required=True)
    args = parser.parse_args()

    settings = Settings(args.db, args.task_name, args.src_file_name)

    dask.set_options(get=dask.multiprocessing.get)
    logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

    logging.info('Pre-processing: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):
        # Loading data
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

        # Splitting column names
        meta_cols = ['best_answer', 'thread_id', 'index', 'post_id']
        # get features columns names
        cols_IV = []
        for col in df_development.columns:
            if col not in meta_cols:
                cols_IV.append(col)

        logging.info('Meta columns: {}'.format(meta_cols))
        logging.info('IV cols: {}'.format(sorted(cols_IV)))

        # Preliminary plots
        logging.info('Attempting plot of raw data.')
        if args.plot:
            logging.info('Plot mode: Enabled. It might take a while.')

            logging.info('Data preparation for plotting started.')
            data_list = []
            variable_list = []
            for index, col in enumerate(cols_IV):
                logging.info('Processing columns: {:3.0f}%'.format(100*index/float(len(cols_IV))))
                data_list.extend(df_development[col].compute())
                variable_list.extend([col] * df_development[col].count().compute())
            df_plot = pd.DataFrame({'data': data_list, 'variable': variable_list})
            logging.info('Data preparation for plotting finished.')

            logging.info('Plotting started')
            bar = BoxPlot(df_plot, values='data',
                          label='variable',
                          plot_width=100*len(cols_IV),
                          plot_height=700,
                          color='variable',
                          legend=False,
                          title='IV distributions (raw data)')
            if args.draft:
                prepare_folder(settings.OUTPUT_PATH_DIR_PLOTS_DRAFT)
                output_file(settings.OUTPUT_PATH_DIR_PLOTS_DRAFT + "boxplots_IV_raw_data.html")
            else:
                prepare_folder(settings.OUTPUT_PATH_DIR_PLOTS)
                output_file(settings.OUTPUT_PATH_DIR_PLOTS + "boxplots_IV_raw_data.html")
            save(bar)
            logging.info('Plotting finished.')

        else:
            logging.info('Plot mode: Disabled... This should save you time.')

        # pre-processing: scaling (http://www.faqs.org/faqs/ai-faq/neural-nets/part2/section-16.html)
        # Scale data

        if args.scaler == 'standard':
            logging.info('Scaler: {}'.format('StandardScaler'))
            mapper = DataFrameMapper([
                (cols_IV, StandardScaler()),
                (meta_cols, None),
            ])
        elif args.scaler == 'robust':
            logging.info('Scaler: {}'.format('RobustScaler'))
            mapper = DataFrameMapper([
                (cols_IV, RobustScaler()),
                (meta_cols, None),
            ])

        # process development data
        dataset_development = mapper.fit_transform(df_development.compute())
        columns = [col for list in [tuple[0] for tuple in mapper.features] for col in list]
        df_development = ddf.from_array(dataset_development, columns=columns)

        # process evaluation data
        dataset_evaluation = mapper.transform(df_evaluation.compute())
        df_evaluation = ddf.from_array(dataset_evaluation, columns=columns)

        # Save data on disk
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

        # Final plotting
        logging.info('Attempting plot of processed data.')
        if args.plot:
            logging.info('Plot mode: Enabled. It might take a while.')

            logging.info('Data preparation for plotting started.')
            data_list = []
            variable_list = []
            for index, col in enumerate(cols_IV):
                logging.info('Processing columns: {:3.0f}%'.format(100 * index / float(len(cols_IV))))
                data_list.extend(df_development[col].compute())
                variable_list.extend([col] * df_development[col].count().compute())
            df_plot = pd.DataFrame({'data': data_list, 'variable': variable_list})
            logging.info('Data preparation for plotting finished.')

            logging.info('Plotting started')
            bar = BoxPlot(df_plot, values='data',
                          label='variable',
                          plot_width=100 * len(cols_IV),
                          plot_height=700,
                          color='variable',
                          legend=False,
                          title='IV distributions (processed data)')
            if args.draft:
                prepare_folder(settings.OUTPUT_PATH_DIR_PLOTS_DRAFT)
                output_file(settings.OUTPUT_PATH_DIR_PLOTS_DRAFT + "boxplots_IV_processed_data.html")
            else:
                prepare_folder(settings.OUTPUT_PATH_DIR_PLOTS)
                output_file(settings.OUTPUT_PATH_DIR_PLOTS + "boxplots_IV_processed_data.html")
            save(bar)
            logging.info('Plotting finished.')
        else:
            logging.info('Plot mode: Disabled... This should save you time.')

        # TODO check for collinearity
        # http://onlinelibrary.wiley.com/doi/10.1890/08-0879.1/abstract

        # TODO others?

    logging.info('Pre-processing: completed.')

if __name__ == "__main__":
    main()
