"""
Title: Boolean Query Parser Module

Project: CSI4107 Project
Version: Vanilla System
Component: Module 6A

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
 Next steps:(done +/-)
 -> expand wildcards in search prior to converting to postfix
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
    exclusion = ["AND", "OR", "AND_NOT", '(',')']
    test_query="(*ge AND_NOT (man* OR health*))"
    test_query = test_query.replace('(', '( ')
    test_query = test_query.replace(')', ' )')
    test_query_list=test_query.split()
    print(test_query_list)
    output_list=[]
    for elements in test_query_list:
        if elements not in exclusion:
            elements=linguistic_module(elements, linguistic_processing_parameters)
            if elements[0].find("*") != -1:
                elements=wildcard_word_finder(elements[0], "uottawa_bigraph_index.csv")
        output_list.append(elements)
    print(output_list)
    test_string=" ".join(output_list)
    print(test_string)




    #test_string=wildcard_word_finder('*ge', "uottawa_bigraph_index.csv")
    # test_string=test_string.replace('(', '( ')
    # test_string =test_string.replace(')', ' )')
    test_string=test_string.split()
    operators=["AND","OR","AND_NOT"]
    opStack = Stack()
    postfixList = []
    for token in test_string:


        if token in operators:
            opStack.push(token)

        elif token =="(":
            opStack.push(token)
        elif token ==")":
            while opStack.peek() != '(':
                postfixList.append(opStack.pop())
        else:
            postfixList.append(token)

    while not opStack.isEmpty():
        if opStack.peek() == '(':
            opStack.pop()
        else:
            postfixList.append(opStack.pop())
    print( " ".join(postfixList))




if __name__ == '__main__':
    main()
