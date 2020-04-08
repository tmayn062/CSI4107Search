"""
Title: Relevance Feedback

Project: CSI4107 Project
Version: Final System
Component: Module 4

Created: 10 Mar 2020
Last modified: 08 Apr 2020

Author: Tiffany Maynard
Status: Completed

Description: Capture the documents that the user finds relevant or non-relevant for a
particular query. This module creates a "relevance memory", keeping track of
relevant and non-relevant documents per query.
relevance_dict is a dictionary with:
query_string as key
(list of relevant doc_ids , list of irrelevant doc_ids) as value
"""
import os
import csv
import ast
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
        print(query_string + ' relevance toggled ' + corpus + str(doc_id))
        relevance_dict[query_string] = toggle_relevance(relevance_dict[query_string], doc_id)
    else:
        print(query_string + ' not in dict yet')
        #add_to_dict either after determine if relevent or non relevant
        #create tuple with doc_id in relevant list
        relevance_dict[query_string] = [doc_id], []
    write_relevance_tocsv(relevance_dict, corpus)

def toggle_relevance(relevance_lists, doc_id):
    """moves doc_id to relevant, non-relevant or no list as a toggle"""
    if doc_id in relevance_lists[0]:
        #if doc_id in relevant list, move to non-relevant
        relevance_lists[0].remove(doc_id)
        relevance_lists[1].append(doc_id)
        print('move to non-relevant')
        print(relevance_lists)
    elif doc_id in relevance_lists[1]:
        #if doc_id in non-relevant list, remove from non-relevant
        relevance_lists[1].remove(doc_id)
        print('remove non-relevant')
        print(relevance_lists)
    else:
    #if doc_id not in any list, add to relevant
        relevance_lists[0].append(doc_id)
        print('add to relevant')
        print(relevance_lists)
    return relevance_lists

def relevant_indicator(query_string, doc_id, corpus):
    """find doc in list and return string to indicate relevant, non-relevant or blank"""
    relevance_dict = get_relevance_dict(corpus)
    if relevance_dict.get(query_string):
        if doc_id in relevance_dict[query_string][0]:
            return "RELEVANT"
        if doc_id in relevance_dict[query_string][1]:
            return "NOT RELEVANT"
    return "NEUTRAL"
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
        print('reading from relevance csv')
        with open(filename, 'r') as data_file:
            reader = csv.reader(data_file)
            for row in reader:
                print(row)
                relevance_dict[row[0]] = (ast.literal_eval(row[1]), ast.literal_eval(row[2]))
        return relevance_dict

    return {}

def write_relevance_tocsv(relevance, corpus):
    """write the relevance file to csv"""
    csv_filename = config.CORPUS[corpus]['relevance_file']
    print('writing relevance')
    print(relevance)
    with open(csv_filename, 'w') as file:
        csv.writer(file).writerows((k,) + v for k, v in relevance.items())
