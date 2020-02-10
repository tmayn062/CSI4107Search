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
#import vsm_weight

def convert_query(query):
    """Convert the query string to a vector."""
    query_list = query.split()
    #TODO add text preprocessing for query here
    return query_list

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
    query_list = convert_query(query)
    score = dict()
    docs = shortlist(query, corpus)
    for doc_id in docs:
        #TODO fill in doclist
        doc_list = []
        score[doc_id] = similarity(doc_list, query_list)
    #Adapted from https://www.geeksforgeeks.org/python-n-largest-values-in-dictionary/
    return nlargest(config.K_RETRIEVAL, score, key=score.get)

def shortlist(query, corpus):
    """Create shortlist of docs from inv_index based only on those that have at
     least one search term from the query."""
    inv_index = read_inverted_index_from_csv(corpus)
    doc_shortlist = dict()
    for word in convert_query(query):
        for doc_id in inv_index[word]:
            #TODO add zeroes when word not present in doc
            doc_shortlist[doc_id] = inv_index[word][doc_id]['weight']
    return doc_shortlist

def read_inverted_index_from_csv(corpus):
    """Read in the inverted index file from disk."""
    if corpus == "uOttawa":
        csv_filename = config.UOTTAWA_VSM_INVERTED_INDEX
    else:
        csv_filename = config.REUTERS_VSM_INVERTED_INDEX

    new_data_dict = {}
    with open(csv_filename, 'r') as data_file:
        for row in data_file:
            row = row.strip().split(",", 1)
            new_data_dict[row[0]] = ast.literal_eval(row[1])
    return new_data_dict
