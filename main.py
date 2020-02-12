"""
Project: CSI4107 Project
Version: Vanilla System
Component: Main

Created: 30 Jan 2020
Last modified: 10 Feb 2020

Author: Jonathan Boerger & Tiffany Maynard
Status: In Progress

Description: Main module - combine all other parts of project
"""
from datetime import datetime
import config
import gui
import corpus_preprocessing
from wildcard_management import wildcard_word_finder
from boolean_search import boolean_search_module
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
from linguistic_processor import linguistic_module
import vsm_retrieval

def main():
    """Run search engine and related functions."""
    start_time = datetime.now()
    print(datetime.now())
    corpus = config.UOTTAWA

    corpus_preprocessing.parse(corpus)
#   TODO create pre-processing parser for Reuters
#   corpus_preprocessing.parse("Reuters")
    dictionary_and_inverted_index_wrapper(config.LINGUISTIC_PARAMS, corpus)
    end_time = datetime.now()
    total_time = end_time-start_time
    print(total_time)
    print(datetime.now())

    tesstt = linguistic_module('crypto*', config.LINGUISTIC_PARAMS)
    print(tesstt)

    print(wildcard_word_finder(tesstt[0], config.CORPUS[corpus]['bigraph_file']))
    boolean_query = '(*ge AND_NOT (man* OR health*))'
    print(boolean_query)
    print(boolean_search_module(boolean_query, corpus))
    print(boolean_search_module("ergodic", corpus))
    print(vsm_retrieval.retrieve("ergodic", corpus))
    gui.SearchEngineGUI()





if __name__ == '__main__':
    main()
