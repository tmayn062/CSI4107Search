"""
Title: Global Query Expansion

Project: CSI4107 Project
Version: Final System
Component: Module 3

Created: 06 Mar 2020
Last modified: 10 Mar 2020

Author: Tiffany Maynard
Status: In Progress

Description: Use an external thesaurus (WordNet) to perform Query Expansion.
Only using synsets in expansion, not hypernyms and only expand when query is
MAX_EXPAND_QUERY_LEN or less (since user is already being very specific if providing
many words in initial query)
"""

from nltk.corpus import wordnet as wn
from numpy import random
import config
class ExpandedQuery:
    """Expanded query holds all the info for providing suggestions"""
    initial_query: str
    expanded_query: str
    suggestions: []
    def __init__(self, initial_query, expanded_query, suggestions):
        """Initialize expanded query"""
        self.initial_query = initial_query
        self.expanded_query = expanded_query
        self.suggestions = suggestions

def create_global_expanded_query(input_query, search_type):
    """Return an expanded VSM or boolean query given a starting query"""
    if search_type == 'VSM' and (len(input_query.split()) <= config.MAX_EXPAND_QUERY_LEN):
        return expand_vsm_query(input_query)
    if search_type == 'Boolean' and (len(input_query.split()) <= (2*config.MAX_EXPAND_QUERY_LEN-1)):
        #allow for boolean terms AND, OR, AND_NOT between query words
        return expand_boolean_query(input_query)
    #input query too long, return input as expanded
    return ExpandedQuery(input_query, input_query, [])

def expand_vsm_query(input_query):
    """Expands a VSM query using WordNet"""
    #used examples from https://pythonprogramming.net/wordnet-nltk-tutorial/
    output = []
    suggestions = []
    for word in input_query.split():
        word_or_syns = [word]
        synset_cap = min(len(wn.synsets(word)), config.EXPANSION_SYNONYMS)
        #allows chance for different synonyms to appear
        #random.choice selects without replacement
        random_synset = random.choice(wn.synsets(word), synset_cap)
        for synset in random_synset:
            for lemma in synset.lemmas():
                if lemma.name().lower() not in word_or_syns:
                    word_or_syns.append(lemma.name().lower())
                    suggestions.append(word + ' ' + lemma.name().lower().replace('_', ' '))
                    # break once we add a lemma from each synset that is not the initial word
                    break
        output.append(' '.join(word_or_syns))
        expanded_query = ' '.join(output).replace('_', ' ')
    return ExpandedQuery(input_query, expanded_query, suggestions)

def expand_boolean_query(input_query):
    """Expands a Boolean query using WordNet
    Replace each term with term in parentheses including ORs for each synonym"""
    #used similar to boolean_query_preprocessing in boolean_search module
    boolean_terms = ["AND", "OR", "AND_NOT", "(", ")"]
    input_query = input_query.replace('(', '( ').replace(')', ' )')
    output = []
    suggestions = []
    for word in input_query.split():
        if word in boolean_terms:
            output.append(word)
        else:
            word_or_syns = [word]
            synset_cap = min(len(wn.synsets(word)), config.EXPANSION_SYNONYMS)
            #allows chance for different synonyms to appear
            #random.choice selects without replacement
            random_synset = random.choice(wn.synsets(word), synset_cap)
            for synset in random_synset:
                for lemma in synset.lemmas():
                    if lemma.name().lower() not in word_or_syns:
                        word_or_syns.append(lemma.name().lower())
                        suggestions.append(
                            '('+word + ' OR ' + lemma.name().lower().replace('_', ' ')+')')
                        # break once we add a lemma from each synset that is not the initial word
                        break
            output.append('('+' OR '.join(word_or_syns).replace('_', ' ')+')')
    expanded_query = ' '.join(output)
    return ExpandedQuery(input_query, expanded_query, suggestions)
