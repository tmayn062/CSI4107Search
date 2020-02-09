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
import config
#import vsm_weight
def retrieve(query, corpus):
    """retrieve ranked list of documents"""
    if (query or corpus):
        return [config.K_RETRIEVAL]
    return []
