# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.preprocess_binaryBestAnswer

This script reads a feature matrix and pre-process it.
"""


import dask
import dask.multiprocessing
dask.set_options(get=dask.multiprocessing.get)

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42



def main():
    print "ciao"
    # TODO: pre-processing: normalization

    # TODO: pre-processing: scaling

    # TODO: others?



if __name__ == "__main__":
    main()