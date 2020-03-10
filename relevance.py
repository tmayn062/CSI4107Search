"""
Title: Relevance Feedback

Project: CSI4107 Project
Version: Final System
Component: Module 4

Created: 10 Mar 2020
Last modified: 10 Mar 2020

Author: Tiffany Maynard
Status: In Progress

Description: Capture the documents that the user finds relevant or non-relevant for a
particular query. This module creates a "relevance memory", keeping track of
relevant and non-relevant documents per query.
relevance_dict is a dictionary with:
query_string as key
(list of relevant doc_ids , list of irrelevant doc_ids) as value
"""
import os
import csv
import config
#Empty globals to store relevance dictionary so it is only read once form csv
RELEVANCE_DICT = {}
RELEVANCE_CORPUS = ""

def update_relevant(query_string, doc_id, corpus):
    """Used to update relevance list for a particular query string, docid, corpus combo"""
    #TODO update to toggle relevance (add/remove from relevent or nonrelevant lists)
    relevance_dict = get_relevance_dict(corpus)
    if relevance_dict.get(query_string):
        #toggle
        print(query_string + 'relevance toggled' + corpus)
    else:
        print(query_string + ' not in dict yet')
        #add_to_dict either after determine if relevent or non relevant

def get_relevance_dict(corpus):
    """Wrapper to avoid multiple dictionary reads from csv."""
    global RELEVANCE_CORPUS
    global RELEVANCE_DICT
    if RELEVANCE_DICT and corpus == RELEVANCE_CORPUS:
        return RELEVANCE_DICT
    RELEVANCE_CORPUS = corpus
    RELEVANCE_DICT = read_relevance_from_csv(corpus)
    return RELEVANCE_DICT

def read_relevance_from_csv(corpus):
    """Read in the csv file that stores the relevance info for a corpus"""
    filename = config.CORPUS[corpus]['relevance_file']
    relevance_dict = dict()
    if os.path.exists(filename):
        with open(filename, 'r') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                relevance_dict[row[0]] = row[1]
        return relevance_dict

    return {}

def write_relevance_tocsv(relevance, csv_filename):
    """Writes the relevance file to csv"""
    with open(csv_filename, 'w') as file:
        [file.write('{0},{1}\n'.format(key, value)) for key, value in relevance.items()]
