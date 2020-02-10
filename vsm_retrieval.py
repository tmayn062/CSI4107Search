"""
Vector Space Model retrieval

Project: CSI4107 Project
Version: Vanilla System
Component: Module 8b

Created: 09 Feb 2020
Last modified: 09 Feb 2020

Author: Tiffany Maynard
Status: In Progress

Description: Implement Vector Space Model from retrieval
"""

from heapq import nlargest
import ast
import numpy as np
import config
import linguistic_processor
#import vsm_weight

def convert_query(query):
    """Convert the query string to a vector."""
    return linguistic_processor.linguistic_module(query, config.LINGUISTIC_PARAMS)

def similarity(doc_list, query_list):
    """Calculate the cosine similarity for the two vectors."""
    #adapted Method 2 from https://stackoverflow.com/a/43943429
    doc_vector = np.array(doc_list)
    query_vector = np.array(query_list)
    doc_norm = doc_vector / np.linalg.norm(doc_vector, axis=0)
    query_norm = query_vector / np.linalg.norm(query_vector, axis=0)
    return np.dot(doc_norm, query_norm)

def retrieve(query, corpus):
    """Retrieve ranked list of documents"""
    #create list of 1's for each word in query, assumes equal weighting for each term
    query_ones = [1 for x in range(len(convert_query(query)))]
    score = dict()
    docs = shortlist(query, corpus)
    for doc_id in docs:
        score[doc_id] = similarity(docs[doc_id], query_ones)
    #Adapted from https://www.geeksforgeeks.org/python-n-largest-values-in-dictionary/
    return nlargest(config.K_RETRIEVAL, score, key=score.get)

def shortlist(query, corpus):
    """Create shortlist of docs from inv_index based only on those that have at
     least one search term from the query."""
    inv_index = read_inverted_index_from_csv(corpus)
    doc_shortlist = dict()
    query_word_list = convert_query(query)
    print("qwl")
    print(query_word_list)
    weight_list_len = len(query_word_list)
    for index, word in enumerate(query_word_list):
        if word in inv_index:
            #allow for queries that contain words not in the corpus
            for doc_id in inv_index[word]:
                if doc_id in doc_shortlist:
                    #doc already added, just update weight entry for this word
                    doc_shortlist[doc_id][index] = inv_index[word][doc_id]['weight']
                else:
                    #doc not added yet add doc_id to shortlist,
                    #initialize list to 0s for all words in query
                    #update weight entry for current word
                    entry = [0 for x in range(weight_list_len)]
                    entry[index] = inv_index[word][doc_id]['weight']
                    doc_shortlist[doc_id] = entry
    return doc_shortlist

def read_inverted_index_from_csv(corpus):
    """Read in the inverted index file from disk."""
    if corpus == config.UOTTAWA_CORPUS:
        csv_filename = config.UOTTAWA_VSM_INVERTED_INDEX
    else:
        csv_filename = config.REUTERS_VSM_INVERTED_INDEX

    new_data_dict = {}
    with open(csv_filename, 'r') as data_file:
        for row in data_file:
            row = row.strip().split(",", 1)
            new_data_dict[row[0]] = ast.literal_eval(row[1])
    return new_data_dict
