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
#import build_dictionary_and_index
#import query

import vsm_retrieval

import spelling
from wildcard_management import wildcard_word_finder
from boolean_search import boolean_search_module
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
from linguistic_processor import linguistic_module

def main():
    """Run search engine and related functions."""
    # TODO : Update to include Reuters parse routine when available
    # remove_stopwords = True
    # do_stemming = True
    # do_normalize = True
    start_time = datetime.now()
    print(datetime.now())


    corpus_preprocessing.parse(config.HTML_FILE, config.UOTTAWA_CORPUS)
    dictionary_and_inverted_index_wrapper(config.LINGUISTIC_PARAMS,
                                          config.UOTTAWA_INVERTED_INDEX,
                                          config.UOTTAWA_CORPUS,
                                          config.UOTTAWA_LPP,
                                          config.UOTTAWA_BIGRAPH)
    end_time = datetime.now()
    total_time = end_time-start_time
    print(total_time)
    print(datetime.now())

    test_string = "U.S.A. hello. he.lp state-of-the-art"
    test_tokens = linguistic_module(test_string, config.LINGUISTIC_PARAMS)
    for token in test_tokens:
        print(token)

    tesstt = linguistic_module('crypto*', config.LINGUISTIC_PARAMS)
    print(tesstt)

    print(wildcard_word_finder(tesstt[0], config.UOTTAWA_BIGRAPH))
    boolean_query = '(*ge AND_NOT (man* OR health*))'
    print(boolean_query)
    print(boolean_search_module(boolean_query,
                                config.LINGUISTIC_PARAMS,
                                config.UOTTAWA_BIGRAPH,
                                config.UOTTAWA_INVERTED_INDEX))


    # TODO : Update to include Reuters dictionary routine when available
    # build_dictionary_and_index.build_it("uOttawaCourseList.xml",
    #                                     remove_stopwords,
    #                                     do_stemming,
    #                                     do_normalize)

    # print(query.process("testing U.S.A. low-cost women babies cacti ",
    #                     remove_stopwords,
    #                     do_stemming,
    #                     do_normalize))
    print(spelling.edit_distance("execution", "intention"))
    print(spelling.edit_distance("sunday", "saturday"))
    print(spelling.edit_distance("dog", "do"))

    corp = "uOttawa"
    qry = "environ lobbi"
    slist = vsm_retrieval.shortlist(qry, corp)
    print(slist)
    ret1 = vsm_retrieval.retrieve(qry, corp)
    print(ret1)
    gui.SearchEngineGUI()





if __name__ == '__main__':
    main()
