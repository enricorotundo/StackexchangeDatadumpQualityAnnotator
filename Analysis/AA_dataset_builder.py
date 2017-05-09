# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.AA_dataset_builder

This script reads a features file and manual annotation file and produces a dataset
"""

import pandas as pd
import dask.dataframe as ddf

from Utils import settings_binaryBestAnswer as settings
from Utils.commons import prepare_folder

def main():
    df_feats = ddf.read_csv(settings.OUTPUT_PATH_DIR + 'features-*.csv', encoding=settings.ENCODING)
    df_ann = pd.read_csv(settings.ANNOTATION_CSV, encoding=settings.ENCODING)

    df_feats = df_feats.compute()
    df_ann.set_index('id', inplace=True)
    df_feats.set_index('post_id', inplace=True)

    df_merge = df_ann.join(df_feats, how='left')
    df_merge.drop('Unnamed: 0', axis=1, inplace=True) # drop weird column

    print df_merge.describe()

    prepare_folder(settings.OUTPUT_PATH_DIR_AA_DATASET)

    df_merge.to_csv(settings.OUTPUT_PATH_DIR_AA_DATASET  + '/AA_annotated_dataset.csv', encoding=settings.ENCODING)

if __name__ == "__main__":
    main()