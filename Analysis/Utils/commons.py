# -*- coding: utf-8 -*-

import os
import glob
import logging


def prepare_folder(path):
    # create output directory
    if not os.path.exists(path):
        logging.info('Creating output directory in {}.'.format(path))
        os.makedirs(path)

    # clear output folder first
    filelist = glob.glob(path + "*.csv")
    for f in filelist:
        logging.info('Clearing output directory: {}.'.format(f))
        os.remove(f)
