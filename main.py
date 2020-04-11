"""
Project: CSI4107 Project
Version: Vanilla System
Component: Main

Created: 30 Jan 2020
Last modified: 13 Feb 2020

Author: Jonathan Boerger & Tiffany Maynard
Status: Complete

Description: Main module - combines all parts of project
"""
from datetime import datetime
import csv
import config
import gui
import corpus_preprocessing
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
from global_query_expansion import create_global_expanded_query
import reuters_preprocessing
import text_categorization

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

    boolean_queries = ['(*ge AND_NOT (man* OR health*))',
                       '(man* OR health*)',
                       '(statistical OR su*ort)',
                       '(operating AND (system OR platform))',
                       '(query AND processing)',
                       'ps*logy',
                       'leadership']
#    for query in boolean_queries:
#        print(query)
#        print(boolean_search.boolean_search_module(query, corpus))
    vsm_queries = ['operoting system',
                   'computers graphical',
                   'lienar',
                   'business administration',
                   'child psychology',
                   'bayesian network classification']
    # for query in vsm_queries[:1]:
    #     print(query)
    #     print(vsm_retrieval.retrieve(query, corpus))
    print(create_global_expanded_query('(hungry AND_NOT green) OR eager', 'Boolean').expanded_query)
    print(create_global_expanded_query('(good AND ready)', 'Boolean').suggestions)
    print(create_global_expanded_query('good ready', 'VSM').suggestions)
    print(create_global_expanded_query('model', 'VSM').expanded_query)
    text_categorization.doc_id_by_topic()
    gui.SearchEngineGUI()





if __name__ == '__main__':
    main()
