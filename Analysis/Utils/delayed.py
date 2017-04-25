# -*- coding: utf-8 -*-
from dask import delayed


@delayed
def selector(df, i):
    """Called by delayed objects, returns a dask.DataFrame"""
    return df.loc[[i]]  # needs double brackets so always return a dask.DataFrame