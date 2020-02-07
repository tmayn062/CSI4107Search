"""
Title: Boolean Search Module

Project: CSI4107 Project
Version: Vanilla System
Component: Module 6

Created: 06 Feb 2020
Last modified: 06 Feb 2020

Author: Jonathan Boerger
Status: WIP

Description:

"""

from pythonds.basic import Stack

from wildcard_management import wildcard_word_finder
from linguistic_processor import linguistic_module

"""
 Next steps:
 -> expand wildcards in search prior to converting to postfix (done +/-)
        |-> replace word with * with expansion
                |-> could be as simple as .replace or query[xx:yy] 
                        |-> difficulty is isolating the word 
                                |-> worst case split the word, expand reconstitute
-> process the query (seperate module)--6B
        |-> apply the stack algorith
                |-> get the doc ids for each word
                        |-> apply the merge algorith for the particular operator
                                |-> pop/push are required to get next operand
                                        |-> get the docids for that word and merge 
                                                |->repead until the query is fully processed
                                                        |-> return docid list 

"""


def main():
    # boolean query linguistic pre-processing and wildcard expansion
    linguistic_processing_parameters = {"do_contractions": True, "do_normalize_hyphens": True,
                                        "do_normalize_periods": True, "do_remove_punctuation": True,
                                        "do_case_fold": True, "do_stop_word_removal": True,
                                        "do_stemming": True, "do_lemming": False}
    test_query="(*ge AND_NOT (man* OR health*))"
    infix_query=boolean_query_preprocessing(test_query, linguistic_processing_parameters, "uottawa_bigraph_index.csv")
    print(infix_query)
    postfix_query=postfix_translation(infix_query)
    print(postfix_query)





def boolean_query_preprocessing(raw_query, linguistic_processing_parameters, bigraph_csv_file):
    """

    :param raw_query:
    :param linguistic_processing_parameters:
    :param bigraph_csv_file:
    :return:
    """
    exclusion = ["AND", "OR", "AND_NOT", '(', ')']
    raw_query = raw_query.replace('(', '( ')
    raw_query = raw_query.replace(')', ' )')
    raw_query_list = raw_query.split()
    output_list = []
    for elements in raw_query_list:
        if elements not in exclusion:
            elements = linguistic_module(elements, linguistic_processing_parameters)
            if elements[0].find("*") != -1:
                elements = wildcard_word_finder(elements[0], bigraph_csv_file)
        output_list.append(elements)
    full_boolean_query = " ".join(output_list)
    return full_boolean_query




def postfix_translation(boolean_infix_query):
    """

    :param boolean_infix_query:
    :return:
    """
    boolean_infix_query = boolean_infix_query.split()
    operators = ["AND", "OR", "AND_NOT"]
    op_stack = Stack()
    postfix_list = []
    for token in boolean_infix_query:

        if token in operators:
            op_stack.push(token)

        elif token == "(":
            op_stack.push(token)
        elif token == ")":
            while op_stack.peek() != '(':
                postfix_list.append(op_stack.pop())
        else:
            postfix_list.append(token)

    while not op_stack.isEmpty():
        if op_stack.peek() == '(':
            op_stack.pop()
        else:
            postfix_list.append(op_stack.pop())
    print(postfix_list)
    return postfix_list
    # postfix_query=" ".join(postfix_list)
    #
    # return postfix_query
    


if __name__ == '__main__':
    main()
