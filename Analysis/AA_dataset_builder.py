# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.AA_dataset_builder

This script reads a features file and manual annotation file and produces a dataset.
NOTE: needs features extracted from 'threads_all_all.json' which is the whole dataset posts+answers, even
those threads without any best_answer.
"""

import pandas as pd
import dask.dataframe as ddf

from Utils.settings import Settings
from Utils.commons import prepare_folder


def main():
    settings = Settings(DB='travel', TASK_NAME='binaryBestAnswer', SRC_FILE_NAME='threads_all_all.json')

    # not the draft!
    df_feats = ddf.read_csv('Analysis/Data/travel/features_threads_all_shared_binaryBestAnswer/' + 'features-*.csv', encoding=settings.ENCODING)
    df_ann = pd.read_csv(settings.ANNOTATION_CSV, encoding=settings.ENCODING)

    df_feats = df_feats.compute()

    ##############
    # NOTE this script need features from threads_all_shared.json!
    print df_feats[df_feats['post_id'] == 1454]
    print "*****************************************************************************"
    print df_feats[df_feats['post_id'] == 1505]
    ############


    df_ann.set_index('id', inplace=True)
    df_feats.set_index('post_id', inplace=True)

    df_merge = df_ann.join(df_feats, how='left')
    #df_merge.drop('Unnamed: 0', axis=1, inplace=True) # drop weird column

    print df_merge.describe()

    prepare_folder(settings.OUTPUT_PATH_DIR_AA_DATASET)

    df_merge.to_csv(settings.OUTPUT_PATH_DIR_AA_DATASET  + '/AA_annotated_dataset.csv', encoding=settings.ENCODING)


if __name__ == "__main__":
    main()
