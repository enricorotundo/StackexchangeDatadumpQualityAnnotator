# -*- coding: utf-8 -*-

"""
Run this with: time python -m Analysis.AA_dataset_builder

This script reads a features file and manual annotation file and produces a dataset
"""

import pandas as pd
import dask.dataframe as ddf

from Utils import settings_binaryBestAnswer as settings


def main():
    df_feats = ddf.read_csv(settings.OUTPUT_PATH_DIR + 'features-*.csv', encoding=settings.ENCODING)
    df_ann = pd.read_csv(settings.ANNOTATION_CSV, encoding=settings.ENCODING)


    df_ann.set_index('id', inplace=True)

    print df_ann.head()


if __name__ == "__main__":
    main()
