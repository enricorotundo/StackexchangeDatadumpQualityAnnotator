# -*- coding: utf-8 -*-

import logging

DB = 'travel'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], 'binaryBestAnswer')
RND_SEED = 42
ENCODING = 'utf-8'
TRAIN_SIZE = 0.7
N_PARTITIONS = 2 # must be > 1?

# logging
LOGGING_FORMAT = '%(asctime)s - %(message)s'
LOGGING_LEVEL = logging.INFO

# draft mode
DRAFT_MODE = True

PROGRESS_BAR_DT = 1 # update every x seconds
PROGRESS_BAR_MIN = 1