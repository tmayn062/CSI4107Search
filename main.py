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
from boolean_search import boolean_search_module
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
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

    boolean_queries = ['(*ge AND_NOT (man* OR health*))',
                       '(statistical OR su*ort)',
                       '(operating AND (system OR platform))',
                       '(query AND processing)',
                       'ps*logy',
                       'leadership']
    for query in boolean_queries[:1]:
        print(query)
        print(boolean_search_module(query, corpus))
    vsm_queries = ['operoting system',
                   'computers graphical',
                   'lienar',
                   'business administration',
                   'child psychology',
                   'bayesian network classification']
    for query in vsm_queries[:1]:
        print(query)
        print(vsm_retrieval.retrieve(query, corpus))

    gui.SearchEngineGUI()





if __name__ == '__main__':
    main()
