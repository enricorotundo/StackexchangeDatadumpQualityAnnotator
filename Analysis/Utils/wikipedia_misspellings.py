# -*- coding: utf-8 -*-

import os

package_directory = os.path.dirname(os.path.abspath(__file__))


data = set()

def load():
    with open(package_directory + '/wikipedia_misspellings.txt', 'r') as f:
        for line in f:
            data.update([line.split('->')[0]])

#NOTE very inefficient
def check(text):
    if not data:
        load()
    if text in data:
        return True
    else:
        return False