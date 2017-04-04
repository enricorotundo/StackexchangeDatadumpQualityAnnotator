
import json
from bs4 import BeautifulSoup

from text_style_features import *


FILE_PATH = 'AnalysisBestAnswer/output/travel/data/threads.json'

with open(FILE_PATH, 'r') as file:
    data = json.load(file)

    for item in data:
        question_body = item['question']['body']
        question_body_stripped = BeautifulSoup(question_body).get_text()
        print question_body_stripped


