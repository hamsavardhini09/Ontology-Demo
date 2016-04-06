import nltk
import os
import re
import json
import unicodedata
import string
import io
import pandas as pd
import textmining
import sklearn
import numpy as np
global collections
import collections
global operator
import operator
global create_tag_image
global make_tags
global LAYOUTS
global get_tag_counts
from nltk import *
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import stem
from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag
import urllib2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from test_word import *
import pickle


#Reading a file
itemlist = find_term()
outfile = open('statementsSum.txt', 'w')
pickle.dump(itemlist, outfile)
x= open("statementsSum.txt").read()
s = unicode(x)
x1 = x.lower()
out = re.sub('[%s]' % re.escape(string.punctuation), '', x)


class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut
    self._stop = set(stopwords.words('english') + list(punctuation))


  def _compute_frequencies(self, word_sent):
    """
      Compute the frequency of each of word.
      Input:
       word_sent, a list of sentences already tokenized.
      Output:
       freq, a dictionary where freq[w] is the frequency of w.
    """


    freq = defaultdict(int)
    for r in word_sent:
      for word in r:
        if word not in self._stop:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in freq.keys():
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences
      which represent the summary of text.
    """
    sent_tok = sent_tokenize(x1)
    assert n <= len(sent_tok)
    word_sent = [word_tokenize(r.lower()) for r in sent_tok]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)
    return [sent_tok[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)


  def stripPunc(self,wordList):
    """Strips punctuation from list of words"""
    puncList = [".",";",":","!","?","/","\\",",","#","@","$","\n","\\n","&",")","(","\""]
    for punc in puncList:
        for word in wordList:
            index = wordList.index(word)
            if punc in word:
                wordList[index] = word.replace(punc,"")
    return wordList

  def final(self):
    fs = FrequencySummarizer()

    y1 = fs.summarize(x1, 1)

    return fs.stripPunc(y1)