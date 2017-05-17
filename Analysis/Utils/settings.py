# -*- coding: utf-8 -*-

import logging


class Settings(object):

    def __init__(self, DB, TASK_NAME, SRC_FILE_NAME):
        """
        DB = 'travel'
        TASK_NAME = 'binaryBestAnswer'
        DATA_DIR_PATH = 'Analysis/Data/' + DB
        SRC_FILE_NAME = 'threads_acceptedOnly_ansCountGte4.json'
        #SRC_FILE_NAME = 'threads_acceptedOnly_all.json'
        """

        # read args
        self.DB = DB
        self.TASK_NAME = TASK_NAME
        self.SRC_FILE_NAME = SRC_FILE_NAME

        # init
        self.DATA_DIR_PATH = 'Analysis/Data/' + self.DB

        # JSON src file
        self.SRC_FILE_PATH = self.DATA_DIR_PATH + '/' + self.SRC_FILE_NAME

        # features
        self.OUTPUT_PATH_DIR = self.DATA_DIR_PATH + '/features_{}_{}/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)
        self.OUTPUT_PATH_DIR_DRAFT = self.DATA_DIR_PATH + '/features_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], self.TASK_NAME)

        # dev/eval splitted features
        self.OUTPUT_PATH_DIR_SPLITTED = self.DATA_DIR_PATH + '/split_{}_{}/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)
        self.OUTPUT_PATH_DIR_SPLITTED_DRAFT = self.DATA_DIR_PATH + '/split_{}_{}_draft/'.format(SRC_FILE_NAME.split(".")[0], TASK_NAME)

        # pre-processed features
        self.OUTPUT_PATH_DIR_PREPROC = self.DATA_DIR_PATH + '/preprocessed_{}_{}/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)
        self.OUTPUT_PATH_DIR_PREPROC_DRAFT = self.DATA_DIR_PATH + '/preprocessed_{}_{}_draft/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)

        # predictions
        self.OUTPUT_PATH_DIR_PREDICTIONS = self.DATA_DIR_PATH + '/predictions_{}_{}/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)
        self.OUTPUT_PATH_DIR_PREDICTIONS_DRAFT = self.DATA_DIR_PATH + '/predictions_{}_{}_draft/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)

        # plots
        self.OUTPUT_PATH_DIR_PLOTS = self.DATA_DIR_PATH + '/plots_{}_{}/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)
        self.OUTPUT_PATH_DIR_PLOTS_DRAFT = self.DATA_DIR_PATH + '/plots_{}_{}_draft/'.format(self.SRC_FILE_NAME.split(".")[0], self.TASK_NAME)

        self.OUTPUT_PATH_DIR_AA_DATASET = self.DATA_DIR_PATH + '/AA_annotated_dataset/'
        self.ANNOTATION_CSV = self.DATA_DIR_PATH + '/' + 'travel_Posts_2017-04-04T09-06-50.604474_sheetV4.csv'
        self.ENCODING = 'utf-8'

        self.RND_SEED = 42
        self.TRAIN_SIZE = 0.7
        self.N_PARTITIONS = 4

        # logging
        self.LOGGING_FORMAT = '%(asctime)s - %(message)s'
        self.LOGGING_LEVEL = logging.INFO

        self.PROGRESS_BAR_DT = 1  # update every x seconds
        self.PROGRESS_BAR_MIN = 5
