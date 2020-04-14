"""
Project: CSI4107 Project
Version: Vanilla System
Component: Main

Created: 30 Jan 2020
Last modified: 13 Apr 2020

Author: Jonathan Boerger & Tiffany Maynard
Status: Complete

Description: Main module - combines all parts of project
"""
from datetime import datetime
import csv
import bs4
from nltk.corpus import reuters
from nltk import FreqDist
import config
import gui
import corpus_preprocessing
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
from global_query_expansion import create_global_expanded_query
import reuters_preprocessing
import text_categorization
import bigram_model
import corpus_access

def main():
    """Run search engine and related functions."""
    csv.field_size_limit(1000000)
    start_time = datetime.now()
    print(datetime.now())
    corpus = config.UOTTAWA

    corpus_preprocessing.parse(corpus)
    reuters_preprocessing.create_reuters_corpus()
    dictionary_and_inverted_index_wrapper(config.LINGUISTIC_PARAMS, corpus)
    corpus = config.REUTERS
    dictionary_and_inverted_index_wrapper(config.LINGUISTIC_PARAMS, corpus)
    end_time = datetime.now()
    total_time = end_time-start_time
    print(total_time)
    print(datetime.now())



    gui.SearchEngineGUI()





if __name__ == '__main__':
    main()
