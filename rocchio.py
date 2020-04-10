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
    print('rv_sum' + str(rv_sum))
    nr_sum = np.add.reduce(nonrelevant_vectors)
    print('nr_sum' + str(nr_sum))
    updated_relevance = cg.ROCCHIO_ALPHA * original \
                        + cg.ROCCHIO_BETA * (1/rv_count if rv_count else 1) * rv_sum \
                        - cg.ROCCHIO_GAMMA * (1/nr_count if nr_count else 1) * nr_sum
    #only keep terms above minimum threshold (also serves to exclude negative values)
    print('before')
    print(updated_relevance[:40])
    updated_relevance = [0 if wgt < cg.ROCCHIO_MIN else wgt for wgt in updated_relevance]
    print('after')
    print(updated_relevance[:40])
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
    for count_vec, word in enumerate(inv_index):
        word_vec[count_vec] = inv_index[word].get(doc_id, {'frequency': 0})['frequency']
    return word_vec

def query_to_word_vector(query_string, corpus):
    """convert a query string to a word vector for a given corpus"""
    inv_index = vsm_retrieval.get_inverted_index(corpus)
    word_vec = np.zeros(len(inv_index))
    query_word_list = vsm_retrieval.convert_query(query_string)
    for count_vec, word in enumerate(inv_index):
        if word in query_word_list:
            word_vec[count_vec] = 1
    return word_vec

def rocchio_expansion(query_string, corpus):
    """get rocchio expansion for query """
    orig = query_to_word_vector(query_string, corpus)
    print('original')
    print(orig[:40])
    rel_list, nonrel_list = relevance.get_relevance_lists(query_string, corpus)
    rel = doc_list_to_array(rel_list, corpus)
    nonrel = doc_list_to_array(nonrel_list, corpus)
    return calc_rocchio(orig, rel, nonrel)

def rocchio_doc_list(query_vector, corpus):
    """get doc_id vectors for a query vector"""
    #create dict of vectors for each docid that contains
    #at least one non-zero term in query_vector
    inv_index = vsm_retrieval.get_inverted_index(corpus)
    doc_shortlist = dict()
    vector_len = len(query_vector)
    word_list = list(inv_index.keys())
    for index, weight in enumerate(query_vector):
        word = word_list[index]
        for doc_id in inv_index[word]:
            if doc_id in doc_shortlist:
                #doc already added, just update weight entry for this word
                doc_shortlist[doc_id][index] = inv_index[word][doc_id]['weight']
            else:
                #doc not added yet add doc_id to shortlist,
                #initialize list to 0s for all words in query
                #update weight entry for current word
                entry = np.zeros(vector_len)
                entry[index] = inv_index[word][doc_id]['weight']
                doc_shortlist[doc_id] = entry

    return doc_shortlist
