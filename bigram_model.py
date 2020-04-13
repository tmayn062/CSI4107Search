"""
Bigram Language model

Project: CSI4107 Project
Version: Final System
Component: Module 2

Created: 11 Apr 2020
Last modified: 13 Apr 2020

Author: Tiffany Maynard
Status: In Progress

Description: Build a Bigram Language Model for each corpus
"""
#adapted from https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-language-model-nlp-python-code/
#also referenced https://www.nltk.org/book/ch02.html
import csv
import ast
import os
import string
from collections import Counter, defaultdict
import bs4
from nltk.corpus import reuters, stopwords
from nltk import bigrams, word_tokenize, FreqDist
import config

BIGRAM_CORPUS = ""
BIGRAM_DICT = {}

def create_bigram_model(corpus):
    """create the bigram model for a corpus"""
    # Create a placeholder for model
    stops = set(stopwords.words("english"))
    model = dict(dict())
    corpus_filename = config.CORPUS[corpus]['corpusxml']
    if corpus == config.UOTTAWA:
        with open(corpus_filename, 'rb') as f:
            data = f.read()
            soup = bs4.BeautifulSoup(data, 'html.parser')
            courses = soup.findAll("course_description")
            for course in courses:
                course_text = course.text.translate(str.maketrans('', '', string.punctuation))
                course_text = course_text.replace('\n', ' ').lower().split()
                filtered_text = [word for word in course_text if word not in stops]
                for w1, w2 in bigrams(filtered_text,
                                      pad_right=True, pad_left=True):
                    if w1 in model:
                        if w2 in model[w1]:
                            model[w1][w2] += 1
                        else:
                            model[w1][w2] = 1
                    else:
                        model[w1] = dict()
                        model[w1][w2] = 1
    else:
        #use reuters.sents from nltk built in for reuters corpus bigrams
        # Count frequency of co-occurance
        fdist = FreqDist(w.lower() for w in reuters.words())
        for sentence in reuters.sents():
            sentence = ' '.join(sentence)
            sentence = sentence.translate(str.maketrans('', '', string.punctuation))
            sentence = sentence.replace('\n', ' ').lower().split()
            filtered_text = [word for word in sentence if word not in stops]
            for w1, w2 in bigrams(filtered_text, pad_right=True, pad_left=True):
                if fdist[w1] > 4:
                    if w1 in model:
                        if w2 in model[w1]:
                            model[w1][w2] += 1
                        else:
                            model[w1][w2] = 1
                    else:
                        model[w1] = dict()
                        model[w1][w2] = 1

    # transform the counts to probabilities
    for w1 in model:
        total_count = float(sum(model[w1].values()))
        for w2 in model[w1]:
            model[w1][w2] /= total_count

    write_bigram_tocsv(model, corpus)


def get_bigram_dict(corpus):
    """Wrapper to avoid multiple dictionary reads from csv."""
    global BIGRAM_CORPUS
    global BIGRAM_DICT
    if BIGRAM_DICT and corpus == BIGRAM_CORPUS:
        return BIGRAM_DICT
    BIGRAM_CORPUS = corpus
    BIGRAM_DICT = read_bigram_from_csv(corpus)
    return BIGRAM_DICT

def write_bigram_tocsv(bi_dict, corpus):
    """write the bigram file to csv"""
    csv_filename = config.CORPUS[corpus]['bigram_file']
    with open(csv_filename, 'w') as file:
        writer = csv.writer(file)
        for key, value in bi_dict.items():
            writer.writerow([key, value])

def read_bigram_from_csv(corpus):
    """Read in the csv file that stores the bigram info for a corpus"""
    filename = config.CORPUS[corpus]['bigram_file']
    bi_dict = dict()
    if os.path.exists(filename):
        print('reading from bigram csv')
        with open(filename, 'r') as data_file:
            reader = csv.reader(data_file)
            for row in reader:
                bi_dict[row[0]] = ast.literal_eval(row[1])
        return bi_dict

    return {}

def create_suggestion_list():
    """create the autocomplete suggestion list based on the corpus"""
    bigram_dict = get_bigram_dict(config.UOTTAWA)
    suggestion_list = []
    for word in bigram_dict:
        for word2 in list(bigram_dict[word])[:config.MAX_QCM_SUGGESTIONS]:
            if word and word2:
                suggestion_list.append(word + ' ' + word2)
    bigram_dict = get_bigram_dict(config.REUTERS)
    for word in bigram_dict:
        for word2 in list(bigram_dict[word])[:config.MAX_QCM_SUGGESTIONS]:
            if word and word2:
                suggestion_list.append(word + ' ' + word2)
    write_suggestion_tocsv(suggestion_list)


def get_suggestion_list():
    """get suggestion list based on both corpuses"""
    return read_suggestion_from_csv()

def write_suggestion_tocsv(suggestion):

    """write the suggestion list to csv"""
    csv_filename = 'autocomplete_list.csv'
    with open(csv_filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(suggestion)

def read_suggestion_from_csv():
    """Read in the csv file that stores the suggestion info """
    filename = 'autocomplete_list.csv'
    suggestion_list = []
    if os.path.exists(filename):
        print('reading from suggestion csv')
        with open(filename, 'r') as data_file:
            reader = csv.reader(data_file)
            for row in reader:
                suggestion_list = row
        return suggestion_list

    return []

def main():
    csv.field_size_limit(100000000)
    create_suggestion_list()

if __name__ == '__main__':
    main()
