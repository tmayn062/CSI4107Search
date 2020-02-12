"""
Title: Boolean Search Module

Project: CSI4107 Project
Version: Vanilla System
Component: Module 6

Created: 06 Feb 2020
Last modified: 10 Feb 2020

Author: Jonathan Boerger
Modified by: Tiffany Maynard
Status: Completed

Description:

The boolean search module implements the boolean search method for information retrieval.

"""


from wildcard_management import wildcard_word_finder
from linguistic_processor import linguistic_module
import config
import vsm_retrieval

def boolean_search_module(query, corpus):

    """
    This is the wrapper method for the entire boolean search module. It ties together all
    supporting modules.
    The method returns a list of relevant docIDs for a given query.

    Of note: as part of the project we assume only informed user are user the system, and are
    only imputing well formatted queries (proper use of brackets and operators). Therefore,
    input validation is not required in this specific use-case.

    :param query: The raw query as entered by the user
    :param corpus: used to lookup bigraph and inverted index files in config

    :return: A list of docIDs
    """
    linguistic_processing_parameters = config.LINGUISTIC_PARAMS
    bigraph_filename = config.CORPUS[corpus]['bigraph_file']
    infix_query = boolean_query_preprocessing(query, linguistic_processing_parameters,
                                              bigraph_filename)
    postfix_query = postfix_translation(infix_query)
    #read in inverted_index dictionary from csv just once per search
    inverted_index_dict = inverted_index_dictionary(corpus)
    doc_id_list = boolean_postfix_query_processor(postfix_query, inverted_index_dict)
    return doc_id_list


def boolean_postfix_query_processor(postfix_query, inverted_index):
    """
    This methods takes a postfix query and actually executes the query to return
    a list of relevant docIDs.

    :param postfix_query: A list containing the postfix query
    :param inverted_index: The filename of the inverted index csv
    :return: A list of docIDs
    """
    operators = ["AND", "OR", "AND_NOT"]
    operand_stack = []
    # if the query is a single word, return the docID list for the word
    if len(postfix_query) == 1:
        if postfix_query[0] in inverted_index:
            return get_doc_id(postfix_query[0], inverted_index)
        return []

    for token in postfix_query:
        if token not in operators:
            operand_stack.append(token)
        else:
            word1 = operand_stack.pop()
            word2 = operand_stack.pop()
            result = intersect_wrapper(word1, word2, token, inverted_index)
            operand_stack.append(result)

    return operand_stack.pop()


def intersect_wrapper(word1, word2, operator, inverted_index):
    """
    The following method applies the required interest method for the query

    Additionally, the method resolves the words into their respective docID list.

    :param word1: The string or list containing the information to be merged
    :param word2: The string or list containing the information to be merged
    :param operator: The logical operator specifying the type of merge operation
    :param inverted_index: The inverted index as dictionary
    :return: A list of merged docIDs

    """
    if isinstance(word1, str):
        word1 = get_doc_id(word1, inverted_index)
        if word1 == -1:
            word1 = []
    if isinstance(word2, str):
        word2 = get_doc_id(word2, inverted_index)
        if word2 == -1:
            word2 = []
    if operator == 'AND':
        result = intersect_and(word1, word2)
    elif operator == 'OR':
        result = intersect_or(word1, word2)
    elif operator == "AND_NOT":
        result = intersect_and_not(word1, word2)
    return result


def intersect_and_not(doc_id_list_2, doc_id_list_1):
    """
    This methods implements the boolean intersect algorithm for AND NOT operations.

    :param doc_id_list_1: List of docIDs associated with word 1
    :param doc_id_list_2: List of docIDs associated with word 2
    :return: List of merged docIDs

    """
    result = []
    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(doc_id_list_1) and pointer2 < len(doc_id_list_2):
        # if the docID is in both list don't add it
        if doc_id_list_1[pointer1] == doc_id_list_2[pointer2]:
            pointer1 += 1
            pointer2 += 1
        # if the docID of L1 is smaller than L2 add the docID to the result list
        elif doc_id_list_1[pointer1] < doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1 += 1
        else:
            pointer2 += 1
    # merging remaining docIDs in list 1
    while pointer1 < len(doc_id_list_1):
        result.append(doc_id_list_1[pointer1])
        pointer1 += 1
    return result


def intersect_and(doc_id_list_1, doc_id_list_2):
    """
        This methods implements the boolean intersect algorithm for AND operations.

        :param doc_id_list_1: List of docIDs associated with word 1
        :param doc_id_list_2: List of docIDs associated with word 2
        :return: List of merged docIDs
    """

    result = []
    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(doc_id_list_1) and pointer2 < len(doc_id_list_2):
        if doc_id_list_1[pointer1] == doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1 += 1
            pointer2 += 1
        elif doc_id_list_1[pointer1] < doc_id_list_2[pointer2]:
            pointer1 += 1
        else:
            pointer2 += 1
    return result


def intersect_or(doc_id_list_1, doc_id_list_2):
    """
    This methods implements the boolean intersect algorithm for OR operations.

    :param doc_id_list_1: List of docIDs associated with word 1
    :param doc_id_list_2: List of docIDs associated with word 2
    :return: List of merged docIDs
    """
    result = []
    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(doc_id_list_1) and pointer2 < len(doc_id_list_2):
        if doc_id_list_1[pointer1] == doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1 += 1
            pointer2 += 1
        elif doc_id_list_1[pointer1] < doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1 += 1
        else:
            result.append(doc_id_list_2[pointer2])
            pointer2 += 1

    # merging remaining docIDs in list 1
    while pointer1 < len(doc_id_list_1):
        result.append(doc_id_list_1[pointer1])
        pointer1 += 1
    # merging remaining docIDs in list 2
    while pointer2 < len(doc_id_list_2):
        result.append(doc_id_list_2[pointer2])
        pointer2 += 1

    return result


def get_doc_id(word_query, inverted_index):
    """
    This methods returns the list of documentIDs which contain the word query.

    :param word_query: The word for which docIDs are to be returned
    :param inverted_index: The inverted index as dictionary
    :return: A list of the documentIDs containing the word
            A -1 if there are no documents which contain the word
    """

    doc_id_list = []
    if word_query in inverted_index:
        for doc_id in inverted_index[word_query]:
            doc_id_list.append(doc_id)

        return doc_id_list
# handling the situation where the dictionary retrieval returns no documents
    return -1


def inverted_index_dictionary(corpus):
    """
    The following method returns inverted index as a dictionary.

    :param corpus: The corpus that produced the inverted index
    :return: Inverted index as a dictionary

    """
    word_dict = vsm_retrieval.read_inverted_index_from_csv(corpus)

    if word_dict:
        return word_dict
    return -1


def boolean_query_preprocessing(raw_query, linguistic_processing_parameters, bigraph_csv_file):
    """
    The following method takes a boolean query and applies linguistic pre-processing to the query,
    to match the LPP done to the inverted index, as well as resolves all wildcards in the query.

    Of note, linguistic pre-processing is performed prior to wildcard resolution.

    :param raw_query: The search query as provided by the user
    :param linguistic_processing_parameters: The dictionary of LPP used to specify which
    linguistic pre-processing parameters to be applied to the query. (For formatting information
    see linguistic_module method in linguistic_processor.py)
    :param bigraph_csv_file: The filename of the bigraph csv file needed to resolve wildcards
    :return: A string containing the properly formatted and processed boolean query
    """
    exclusion = ["AND", "OR", "AND_NOT", "(", ")"]
    # separating the parentheses from its associated word to facilitate future processing
    raw_query = raw_query.replace('(', '( ')
    raw_query = raw_query.replace(')', ' )')
    raw_query_list = raw_query.split()
    output_list = []
    for elements in raw_query_list:
        # if the element is an actual word apply the LPP to it
        if elements not in exclusion:
            element = linguistic_module(elements, linguistic_processing_parameters)
            # if the word contains an asterisks, resolve the wildcard

            if element[0].find("*") != -1:
                element = wildcard_word_finder(element[0], bigraph_csv_file)
            else:
                element = element[0]
            output_list.append(element)
        else:
            output_list.append(elements)

    full_boolean_query = " ".join(output_list)
    return full_boolean_query


def postfix_translation(boolean_infix_query):
    """
    This methods converts a boolean query from infix notation to postfix notation.

    This method was developed based on the information provided at:
    https://runestone.academy/runestone/books/published/pythonds/BasicDS/
        InfixPrefixandPostfixExpressions.html#fig-evalpost2
    Specifically, it was adapted from the code provided in the 'Active Code 1' section

    :param boolean_infix_query: A string containing the infix query
    :return: A list containing the postfix query
    """
    boolean_infix_query = boolean_infix_query.split()
    #precedence
    prec = {}
    prec["AND"] = 1
    prec["OR"] = 1
    prec["AND_NOT"] = 1
    prec["("] = 3

    operators = ["AND", "OR", "AND_NOT", "(", ")"]
    op_stack = []
    postfix_list = []
    for token in boolean_infix_query:
        if token not in operators:
        # appending regular words directly to the result list
            postfix_list.append(token)
        elif token == '(':
        # pushing the opening parentheses onto the stack
            op_stack.append(token)
        elif token == ')':
        # if a closing parentheses is processed, all items on the stack between the respective
        # parentheses is appended to the result list
            while (op_stack and op_stack[-1] != '('):
                postfix_list.append(op_stack.pop())
            if (op_stack and op_stack[-1] != '('):
                return -1
            op_stack.pop()
        else:
        # pushing the logical operator onto the stack
            while op_stack and (prec[op_stack[-1]] < prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.append(token)
    # extracting all remaining logical operators from the stack
    while op_stack:
        postfix_list.append(op_stack.pop())
    return postfix_list
