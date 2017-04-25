# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.preprocess_binaryBestAnswer

This script reads a feature matrix and pre-process it.
"""

import logging

import dask.multiprocessing

from Utils import settings_binaryBestAnswer as settings

dask.set_options(get=dask.multiprocessing.get)
logging.basicConfig(format=settings.LOGGING_FORMAT, level=settings.LOGGING_LEVEL)

def main():
    logging.info('Pre-processing: started.')

    # TODO: pre-processing: normalization

    # TODO: pre-processing: scaling

    # TODO: others?

    logging.info('Pre-processing: completed.')

if __name__ == "__main__":
    main()