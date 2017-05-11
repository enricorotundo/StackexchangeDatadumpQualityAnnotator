# -*- coding: utf-8 -*-

import logging

DB = 'travel'
TASK_NAME = 'binaryBestAnswer'
DATA_DIR_PATH = 'Analysis/Data/' + DB
SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
#SRC_FILE_NAME = 'threads_acceptedOnly_all.json'

# JSON src file
SRC_FILE_PATH = DATA_DIR_PATH + '/' + SRC_FILE_NAME

# features
OUTPUT_PATH_DIR = DATA_DIR_PATH + '/features_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)
OUTPUT_PATH_DIR_DRAFT = DATA_DIR_PATH + '/features_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)

# dev/eval splitted features
OUTPUT_PATH_DIR_SPLITTED = DATA_DIR_PATH + '/split_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)
OUTPUT_PATH_DIR_SPLITTED_DRAFT = DATA_DIR_PATH + '/split_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)

# pre-processed features
OUTPUT_PATH_DIR_PREPROC = DATA_DIR_PATH + '/preprocessed_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)
OUTPUT_PATH_DIR_PREPROC_DRAFT = DATA_DIR_PATH + '/preprocessed_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)

# predictions
OUTPUT_PATH_DIR_PREDICTIONS = DATA_DIR_PATH + '/predictions_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)
OUTPUT_PATH_DIR_PREDICTIONS_DRAFT = DATA_DIR_PATH + '/predictions_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)

# plots
OUTPUT_PATH_DIR_PLOTS = DATA_DIR_PATH + '/plots_{}_{}/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)
OUTPUT_PATH_DIR_PLOTS_DRAFT = DATA_DIR_PATH + '/plots_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)

OUTPUT_PATH_DIR_AA_DATASET = DATA_DIR_PATH + '/AA_annotated_dataset/'
ANNOTATION_CSV = DATA_DIR_PATH + '/' + 'travel_Posts_2017-04-04T09-06-50.604474_sheetV4.csv'
ENCODING = 'utf-8'

RND_SEED = 42
TRAIN_SIZE = 0.7
N_PARTITIONS = 4

# logging
LOGGING_FORMAT = '%(asctime)s - %(message)s'
LOGGING_LEVEL = logging.INFO

PROGRESS_BAR_DT = 1  # update every x seconds
PROGRESS_BAR_MIN = 5
