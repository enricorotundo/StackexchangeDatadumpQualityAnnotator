# -*- coding: utf-8 -*-

"""
run this with: python -m Analysis.feats_extract
"""

import json
import csv

from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

from Analysis.Features import text_style

nltk.data.path.append('venv/nltk_data')

DB = 'travel'
FILE_PATH = 'Analysis/Data/' + DB + '/threads.json'


def main():
    with open(FILE_PATH, 'r') as file:
        data = json.load(file, encoding='utf-8')

        dataset = []

        print len(data)

        for item in data:
            datapoint = dict()


            question_body = item['question']['body']
            question_body_stripped = BeautifulSoup(question_body, "html5lib").get_text()

            #TODO extract best answer feats

            #TODO extract other answers feats

            #TODO add other funcs
            funcs = [text_style.ty_cpc,
                     text_style.ty_cpe]

            for f in funcs:
                datapoint[f.__name__] = f(question_body_stripped)

            dataset.append(datapoint)

        print dataset[0]


        with open('output.csv', 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, dataset[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(dataset)

if __name__ == "__main__":
    main()