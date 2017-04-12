# -*- coding: utf-8 -*-

import re

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn

from Analysis.Utils import wikipedia_misspellings
from Analysis.Libs.nltk_passive_voice import passive

nltk.data.path.append('venv/nltk_data')

"""
sets from:
`Automatic Assessment of Document Quality in Web Collaborative Digital Libraries`
Dalip et al. 2011
"""
AUXIL_VERBS = set(['will', 'shall', 'cannot', 'may', 'need to', 'would', 'should', 'could', 'might', 'must', 'ought',
                  'ought to', 'can’t', 'can'])
PRONOUNS = set(['i', 'me', 'we', 'us', 'you', 'he', 'him', 'she', 'her', 'it', 'they', 'them', 'thou', 'thee', 'ye',
               'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'yourselves', 'themselves', 'oneself',
               'my', 'mine', 'his', 'hers', 'yours', 'ours', 'theirs', 'its', 'our', 'that', 'their', 'these', 'this',
               'those', 'your'])
CONJS = set(['and', 'but', 'or', 'yet', 'nor'])
PREPOSITIONS = set(['aboard', 'about', 'above', 'according to', 'across from', 'after', 'against', 'alongside',
                    'alongside of', 'along with', 'amid', 'among', 'apart from', 'around', 'aside from', 'at',
                    'away from', 'back of', 'because of', 'before', 'behind', 'below', 'beneath', 'beside', 'besides',
                    'between', 'beyond', 'but', 'by means of', 'concerning', 'considering', 'despite', 'down',
                    'down from', 'during', 'except', 'except for', 'excepting for', 'from among', 'from between',
                    'from under', 'in addition to', 'in behalf of', 'in front of', 'in place of', 'in regard to',
                    'inside of', 'inside', 'in spite of', 'instead of', 'into', 'like', 'near to' , 'off',
                    'onaccount of', 'onbehalf of', 'onto', 'ontop of', 'on', 'opposite', 'out of', 'out', 'outside',
                    'outside of', 'over to', 'over', 'owing to', 'past', 'prior to', 'regarding', 'round about',
                    'round', 'since', 'subsequent to', 'together', 'with', 'throughout', 'through', 'till', 'toward',
                    'under', 'underneath', 'until', 'unto', 'up', 'up to', 'upon', 'with', 'within', 'without',
                    'across', 'along', 'by', 'of', 'in', 'to', 'near', 'of', 'from'])
TOBE_VERBS = set(['be', 'being', 'was', 'were', 'been', 'are', 'is'])
ARTICLES = set(['the', 'a', 'an'])

SUB_CONJS = set(['after', 'because', 'lest', 'till', '’til', 'although', 'before', 'now that', 'unless',
                 'as', 'even if', 'provided that', 'provided', 'until', 'as if', 'even though', 'since', 'as long as',
                 'so that', 'whenever', 'as much as', 'if', 'than', 'as soon as', 'inasmuch', 'in order that',
                 'though', 'while'] )
INTERR_PRONOUNS = set(['why', 'who', 'what', 'whom', 'when', 'where', 'how'])

#TODO before using these functions check for stemming, normalization and encoding!!!

def ty_cpc(text):
    """Return the number of words capitalized in @text"""
    regex = r"\b[A-Z]\S+"
    matches = re.findall(regex, text)
    result = len(matches)
    return result


def ty_cpe(text):
    """Return the number of capitalization errors in @text. 
    First letter of a sentence not capitalized"""
    result = 0
    for sent in sent_tokenize(text):
        if len(sent) > 0:
            if not sent[0].isupper():
                result = result + 1
    return result


def ty_poc(text):
    """Return excessive punctuation count.
    Repeated ellipsis, repeated question marks, repeated spacing (irregular).
    """
    result = 0
    # ellipsis
    regex = r"[.]{3}[.]+"
    result = result + len(re.findall(regex, text))
    # repeated question marks
    regex = r"[?]{1}[?]+"
    result = result + len(re.findall(regex, text))
    # irregular spacing
    regex = r"[ ]{1}[ ]+"
    result = result + len(re.findall(regex, text))
    return result

def ty_pde(text):
    """Return punctuation density (percent of all characters)"""
    regex = r"[^a-zA-Z ]"
    result = len(re.findall(regex, text)) / float(len(text))
    return result

def ty_sde(text):
    """Return spacing density (percent of all characters)"""
    regex = r"[ ]"
    result = len(re.findall(regex, text)) / float(len(text))
    return result

#TODO
# https://en.wikipedia.org/wiki/Entropy_(information_theory)
# similar to password strength?
def ty_wse(text):
    """Return entropy of the text word sizes (character-level entropy of the text).
    """
    result = 0
    return result

#TODO
def ty_inn(text):
    """
    returns: information to noise
    """
    return 0

def ty_nwnt(text):
    """Return number of words not in WordNet"""
    result = 0
    regex = r"[a-zA-Z]+"
    tokens = word_tokenize(text)
    for token in tokens:
        if re.match(regex, token):
            if token not in wn.words():
                result = result + 1
    return result

def ty_typo(text):
    """Return number of typos.
    Words not in common typos list https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings
    """
    result = 0
    regex = r"[a-zA-Z]+"
    tokens = word_tokenize(text)
    for token in tokens:
        if re.match(regex, token):
            if wikipedia_misspellings.check(token):
                result = result + 1
    return result

def ty_slp(text):
    """Return the size of largest phrase"""
    result = 0
    if len(text) > 0:
        largest_phrase = max(sent_tokenize(text), key=len)
        result = len(largest_phrase)
    return result

#TODO
def ty_lpr(text):
    """
    returns: %p where (length - avg. length) >= 10 words
    """
    return 0

#TODO
def ty_spr(text):
    """
    returns: %p where (avg. length - length) >= 5 words
    """
    return 0

def ty_avc(text):
    """Return the number of auxiliary verbs"""
    result = 0
    tokens = word_tokenize(text)
    for token in tokens:
        if token in AUXIL_VERBS:
            result = result + 1
    return result

#TODO
def ty_qc(text):
    """
    returns: number of questions
    """
    return 0

def ty_pc(text):
    """Returns number of pronouns"""
    result = 0
    tokens = word_tokenize(text)
    prons_presence = map(lambda token: 1 if token in PRONOUNS else 0, tokens)
    result = reduce(lambda x,y: x+y, prons_presence)
    return result

def ty_pvc(text):
    """Return numbrer of passive voice sentences"""
    # read README.md of passive, first run
    passive_senteces = passive.findpassives_string(text)
    result = len(passive_senteces)
    return result

def ty_cjr(text):
    """Return the number of words that are conjunctions"""
    result = 0
    tokens = word_tokenize(text)
    for token in tokens:
        if token in CONJS:
            result = result + 1
    return result

#NOTE not a feature
def t_lw(text):
    """Return number of (full) words"""
    result = 0
    for token in word_tokenize(text):
        # count nr words
        if re.search(r"^[a-zA-Z]+$", token):
            result = result + 1
    return result

def ty_nr(text):
    """Return the nominalizations rate. 
    Nominalization-rate = sbCount / t-lw
    """
    regex = r"(?:tion|ment|ence|ance)"
    sbCount = len(re.findall(regex, text)) # nr of nominalizations
    result = sbCount / float(t_lw(text))
    return result

def ty_pr(text):
    """Return the prepositions rate. 
    """
    prepCount = 0
    tokens = word_tokenize(text)
    for token in tokens:
        if token in PREPOSITIONS:
            prepCount = prepCount + 1
    result = prepCount / float(t_lw(text))
    return result

def ty_ber(text):
    """Returns the number of uses of verb "to be"""
    toBeCount = 0
    tokens = word_tokenize(text)
    for token in tokens:
        if token in TOBE_VERBS:
            toBeCount = toBeCount + 1
    result = toBeCount / float(t_lw(text))
    return result

def ty_sp(text):
    """Return #p (nr. of phrases) starting with a pronoun"""
    tokens = sent_tokenize(text)
    result = 0
    for sentence in tokens:
        first_word = word_tokenize(sentence)[0]
        if first_word in PRONOUNS:
            result = result + 1
    return result

def ty_sa(text):
    """Return #p starting with an article"""
    tokens = sent_tokenize(text)
    result = 0
    for sentence in tokens:
        first_word = word_tokenize(sentence)[0]
        if first_word in ARTICLES:
            result = result + 1
    return result

def ty_scc(text):
    """Return #p starting with a conjunction"""
    tokens = sent_tokenize(text)
    result = 0
    for sentence in tokens:
        first_word = word_tokenize(sentence)[0]
        if first_word in CONJS:
            result = result + 1
    return result

def ty_sscc(text):
    """Return #p starting with a subordinating conjunction"""
    tokens = sent_tokenize(text)
    result = 0
    for sentence in tokens:
        first_word = word_tokenize(sentence)[0]
        if first_word in SUB_CONJS:
            result = result + 1
    return result

def ty_sipc(text):
    """Return #p starting with an interrogative pronoun"""
    tokens = sent_tokenize(text)
    result = 0
    for sentence in tokens:
        first_word = word_tokenize(sentence)[0]
        if first_word in INTERR_PRONOUNS:
            result = result + 1
    return result

def ty_spr(text):
    """Return #p starting with a preposition"""
    tokens = sent_tokenize(text)
    result = 0
    for sentence in tokens:
        first_word = word_tokenize(sentence)[0]
        if first_word in PREPOSITIONS:
            result = result + 1
    return result

#TODO
def ty_klg(text):
    """
    returns: KLD(good answers)
    """
    return 0

#TODO
def ty_klt(text):
    """
    returns: KLD(good answers of same category)
    """
    return 0

#TODO
def ty_klwid(text):
    """
    returns: KLD(Wikipedia discussion pages)
    """
    return 0

#TODO
def ty_klwi(text):
    """
    returns: KLD(Wikipedia pages classified as "Good"
    """
    return 0