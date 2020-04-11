"""
Bigram Language model

Project: CSI4107 Project
Version: Final System
Component: Module 2

Created: 11 Apr 2020
Last modified: 11 Apr 2020

Author: Tiffany Maynard
Status: In Progress

Description: Build a Bigram Language Model for each corpus
"""
#adapted from https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-language-model-nlp-python-code/
#also referenced https://www.nltk.org/book/ch02.html
import bs4
from nltk.corpus import reuters
from nltk import bigrams
from collections import Counter, defaultdict
import config

def create_bigram_model(corpus):
    """create the bigram model for a corpus"""
    # Create a placeholder for model
    model = defaultdict(lambda: defaultdict(lambda: 0))
    corpus_filename = config.CORPUS[corpus]['corpusxml']
    with open(corpus_filename, 'rb') as f:
        data = f.read()
        soup = bs4.BeautifulSoup(data, 'html.parser')
        articles = soup.findAll("article")
        # for article in articles:
        #     body = article.find("body").text
    # Count frequency of co-occurance
    for sentence in reuters.sents():
        for w1, w2 in bigrams(sentence, pad_right=True, pad_left=True):
            model[w1][w2] += 1

    # Let's transform the counts to probabilities
    for w1 in model:
        total_count = float(sum(model[w1].values()))
        for w2 in model[w1]:
            model[w1][w2] /= total_count
