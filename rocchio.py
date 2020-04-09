"""
Title:  Local Query Expansion with Rocchio Algorithm

Project: CSI4107 Project
Version: Final System
Component: Module 5

Created: 08 Apr 2020
Last modified: 09 Apr 2020

Author: Tiffany Maynard
Status: In Progress

Description: Perform implicit query expansion using the relevance provided, within the VSM,
using the Rocchio Algorithm.
relevance_dict is a dictionary with:
query_string as key
(list of relevant doc_ids , list of irrelevant doc_ids) as value
"""
import numpy as np
import config as cg
import vsm_retrieval
import relevance

def calc_rocchio(original, relevant_vectors, nonrelevant_vectors):
    """calculate new relevance using rocchio algorithm
    original, relevant, nonrelevant must be vectors for same words"""
    rv_count = len(relevant_vectors)
    nr_count = len(nonrelevant_vectors)
    rv_sum = np.add.reduce(relevant_vectors)
    nr_sum = np.add.reduce(nonrelevant_vectors)
    updated_relevance = cg.ROCCHIO_ALPHA * original \
                        + cg.ROCCHIO_BETA * (1/rv_count if rv_count else 1) * rv_sum \
                        - cg.ROCCHIO_GAMMA * (1/nr_count if nr_count else 1) * nr_sum
    #only keep terms above minimum threshold (also serves to exclude negative values)
    print('before')
    print(updated_relevance)
    updated_relevance = [0 if wgt < cg.ROCCHIO_MIN else wgt for wgt in updated_relevance]
    print('after')
    print(updated_relevance)
    return updated_relevance

def doc_list_to_array(rel_list, corpus):
    """convert a list doc ids to a list of word arrays"""
    word_arrays = []
    for doc_id in rel_list:
        word_arrays.append(get_word_vector(doc_id, corpus))
    return word_arrays

def get_word_vector(doc_id, corpus):
    """create vector with every word in inverted index and populate for doc_id"""
    inv_index = vsm_retrieval.get_inverted_index(corpus)
    word_vec = np.zeros(len(inv_index))
    count_vec = 0
    for word in inv_index:
        word_vec[count_vec] = inv_index[word].get(doc_id, {'frequency': 0})['frequency']
        count_vec += 1
    return word_vec

def query_to_word_vector(query_string, corpus):
    """convert a query string to a word vector for a given corpus"""
    inv_index = vsm_retrieval.get_inverted_index(corpus)
    word_vec = np.zeros(len(inv_index))
    query_word_list = vsm_retrieval.convert_query(query_string)
    count_vec = 0
    for word in query_word_list:
        if inv_index[word]:
            word_vec[count_vec] = 1
        count_vec += 1
    return word_vec

def rocchiotest():
    """test rocchio calcs"""
    corpus = cg.UOTTAWA
    q_string = 'women math'
    orig = query_to_word_vector(q_string, corpus)
    rel_list, nonrel_list = relevance.get_relevance_lists(q_string, corpus)
    rel = doc_list_to_array(rel_list, corpus)
    nonrel = doc_list_to_array(nonrel_list, corpus)
    a_test = calc_rocchio(orig, rel, nonrel)
    print(a_test)
