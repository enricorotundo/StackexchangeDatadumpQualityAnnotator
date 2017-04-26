# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.preprocess_binaryBestAnswer

This script reads a feature matrix and pre-process it.
"""

import logging

import dask.multiprocessing
from dask.diagnostics import ProgressBar

from Utils import settings_binaryBestAnswer as settings

dask.set_options(get=dask.multiprocessing.get)
logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

def main():
    logging.info('Pre-processing: started.')

    with ProgressBar(dt=settings.PROGRESS_BAR_DT, minimum=settings.PROGRESS_BAR_MIN):
        # TODO: pre-processing: normalization
        print "ciao"
        # TODO: pre-processing: scaling

        # TODO: others?

    logging.info('Pre-processing: completed.')

if __name__ == "__main__":
    main()