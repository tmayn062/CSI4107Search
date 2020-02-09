"""
Vector Space Model weight calculation

Project: CSI4107 Project
Version: Vanilla System
Component: Module 8a

Created: 09 Feb 2020
Last modified: 09 Feb 2020

Author: Tiffany Maynard
Status: In Progress

Description: Include term weights in the index
"""
import numpy as np

def calc_weights(index):
    """Calculate td-idf weights for all documents in collection"""

    if index:
        return [0]
    return []

def similarity(doc_list, query_list):
    """Calculate the cosine similarity for the two vectors."""
    #adapted Method 2 from https://stackoverflow.com/a/43943429
    doc_vector = np.array(doc_list)
    query_vector = np.array(query_list)
    doc_norm = doc_vector / np.linalg.norm(doc_vector, axis=0)
    query_norm = query_vector / np.linalg.norm(query_vector, axis=0)
    return np.dot(doc_norm, query_norm)
