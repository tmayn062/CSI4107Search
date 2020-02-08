"""
Title: Wildcard Management Module

Project: CSI4107 Project
Version: Vanilla System
Component: Module 7

Created: 02 Feb 2020
Last modified: 06 Feb 2020

Author: Jonathan Boerger
Status: Effectively complete- small tweaks remaining

Description: 

The wildcard management module resolves wildcards into all possible words
which satisfy the wildcard
"""
import pandas as pd
from linguistic_processor import bigraph_splitter


def wildcard_word_finder(wildcard_search_word, bigraph_index_filename):
    """
    This method resolves a wildcard search to return all possible words
    which satisfies the wildcard. 

    Of note: if the query does not actually have an asteriks, the output is simply
    the original word. Therefore, the method does not require input validation.
    
    :param wildcard_search_word: The wildcard search word to be resolved
    :param bigraph_index_filename: The CSV file containing the bigraph inverted index
    :return: A list of words which satisfies the wildcard search

    TODO: dealing with multiple wildcards (if so choose to)
    """
    asterisks_position = wildcard_search_word.find('*')
    # removing the * from the search word
    stripped_search_word = wildcard_search_word.replace("*", "")
    # transforming the word into bigraphs
    search_word_bigraphs = bigraph_splitter(stripped_search_word)

    # extracting the bigraph from the bigraph-search word pair
    bigraph_list = []
    for bigraph in search_word_bigraphs:
        bigraph_list.append(bigraph[0])

    # getting all possible words for the given bigraphs
    potential_words_strings = bigraph_word_find_in_index(bigraph_list, bigraph_index_filename)

    # the words associated to the bigraph are returned as a string. Therefore the following
    # does some string post processing and splits the words in a string into words in a list
    potential_word_list = []
    for word_string in potential_words_strings:
        word_string = word_string.replace(']', '')
        word_string_split = word_string.split(',')
        for word in word_string_split:
            potential_word_list.append(word[2:len(word) - 1])

    # the following sections trims all the possible words associated with the bigraph to those
    # which conform with the requirements of the wildcard
    potential_word_list.sort()
    duplicate_word_list = []
    # If the wild card has the form *xxxx i.e. looking for a specific ending of a word
    if asterisks_position == 0:
        for potential_word in potential_word_list:
            if potential_word.endswith(stripped_search_word):
                duplicate_word_list.append(potential_word)
    # If the wildcard has the form xxxx* i.e. looking for a specific beginning of a word
    elif asterisks_position == len(wildcard_search_word) - 1:
        for potential_word in potential_word_list:
            if potential_word.startswith(stripped_search_word):
                duplicate_word_list.append(potential_word)
    # If the wildcard has the form xx*xx i.e the word has specific beginning and ending
    else:
        for potential_word in potential_word_list:
            if potential_word.startswith(wildcard_search_word[:asterisks_position]) \
                    and potential_word.endswith(wildcard_search_word[asterisks_position + 1:]):
                duplicate_word_list.append(potential_word)
    # Removing all duplicate words from the valid word list
    actual_word_list = []
    for duplicate_word in duplicate_word_list:
        if duplicate_word in actual_word_list:
            pass
        else:
            actual_word_list.append(duplicate_word)

    # transforming result into a string where words are separated by OR such that it
    # can be used in a boolean search
    if len(actual_word_list) == 0:
        return ""
    or_string = f'{actual_word_list[0]}'
    if len(actual_word_list) > 1:
        or_string='( '+or_string
        for x in range(1, len(actual_word_list)):
            or_string = or_string + f' OR {actual_word_list[x]}'
        or_string = or_string + ' )'

    return or_string


def bigraph_word_find_in_index(bigraph_query_list, index):
    """
    This method finds the words associated with a bigraph

    Since the query_list and the index are both sorted alphabetically the search and retrieve
    takes O(n).

    :param bigraph_query_list: List of bigraph to be searched for
    :param index: The index to be searched
    :return: List of resulting words associated with the bigraph
    """
    bigraph_query_list.sort()
    data = pd.read_csv(index)
    point = 0
    result_list = []
    for xxxx in range(0, data.shape[0]):
        if data.iloc[xxxx, 0] == bigraph_query_list[point]:
            result_list.append(data.iloc[xxxx, 1])
            point += 1
        # elif str(data.iloc[xxxx + 1, 0]) > query[point]:
        #     point += 1
        if point == len(bigraph_query_list):
            break
    return result_list
