# -*- coding: utf-8 -*-

def getX(df):
    result = df.drop('best_answer', axis=1) \
                .drop('thread_id', axis=1) \
                .drop('index', axis=1).compute()
    return result