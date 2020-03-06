"""
Title: Global Query Expansion

Project: CSI4107 Project
Version: Final System
Component: Module 3

Created: 06 Mar 2020
Last modified: 06 Mar 2020

Author: Tiffany Maynard
Status: In Progress

Description: Use an external thesaurus (WordNet) to perform Query Expansion.

"""

from nltk.corpus import wordnet

def create_global_expanded_query(input_query, search_type):
    """Return an expanded VSM or boolean query given a starting query"""
    if search_type == 'VSM':
        return expand_vsm_query(input_query)
    return expand_boolean_query(input_query)

def expand_vsm_query(input_query):
    """Expands a VSM query using WordNet
    TODO add similarity weights to query terms"""
    #used examples from https://pythonprogramming.net/wordnet-nltk-tutorial/
    output = input_query.split()
    for word in input_query:
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                output.append(lemma.name())
    return ' '.join(output)

def expand_boolean_query(input_query):
    """Expands a Boolean query using WordNet
    Replace each term with term in parentheses including ORs for each synonym"""
    #used similar to boolean_query_preprocessing in boolean_search module
    boolean_terms = ["AND", "OR", "AND_NOT", "(", ")"]
    input_query = input_query.replace('(', '( ').replace(')', ' )')
    output = []
    for word in input_query.split():
        if word in boolean_terms:
            output.append(word)
        else:
            word_or_syns = [word]
            for synset in wordnet.synsets(word):
                for lemma in synset.lemmas():
                    if lemma.name() not in word_or_syns:
                        word_or_syns.append(lemma.name())
            output.append('('+' OR '.join(word_or_syns)+')')
    return ' '.join(output)
