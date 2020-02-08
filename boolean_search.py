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
import pandas as pd
import ast

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
    test_query="(leadership AND crypto*)"
    infix_query=boolean_query_preprocessing(test_query, linguistic_processing_parameters, "uottawa_bigraph_index.csv")
    print(f'infix query: {infix_query}')
    postfix_query=postfix_translation(infix_query)
    print(f'Post fix query: {postfix_query}')
    operators = ["AND", "OR", "AND_NOT"]
    operand_stack=Stack()

    if len(postfix_query)==1:
        print(get_doc_id(postfix_query[0], "uottawa_inverted_index.csv"))

    for token in postfix_query:
        if token not in operators:
            operand_stack.push(token)
        else:
            word1=operand_stack.pop()
            word2=operand_stack.pop()
            result= intersect_wrapper(word1,word2, token, "uottawa_inverted_index.csv")
            operand_stack.push(result)
    print(operand_stack.pop())
    # doc_id_list_1= get_doc_id('architectur', 'uottawa_inverted_index.csv')
    # print(doc_id_list_1)
    # doc_id_list_2=get_doc_id('www', 'uottawa_inverted_index.csv')
    # print(doc_id_list_2)
    # print(intersect_and_not(doc_id_list_1,doc_id_list_2))


def intersect_wrapper(word1, word2, operator, inverted_index):
    if type(word1) == str:
        word1 = get_doc_id(word1, inverted_index)
    if type(word2) == str:
        word2 = get_doc_id(word2, inverted_index)
    if operator == 'AND':
        return intersect_and(word1, word2)
    elif operator == 'OR':
        return  intersect_or(word1, word2)
    elif operator == "AND_NOT":
        return  intersect_and_not(word1, word2)

def intersect_and_not(doc_id_list_1, doc_id_list_2):
    result=[]
    pointer1=0
    pointer2=0
    while pointer1<len(doc_id_list_1) and pointer2<len(doc_id_list_2):
        if doc_id_list_1[pointer1]==doc_id_list_2[pointer2]:
            pointer1+=1
            pointer2+=1
        elif doc_id_list_1[pointer1]<doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1+=1
        else:
            pointer2+=1
    while pointer1<len(doc_id_list_1):
        result.append(doc_id_list_1[pointer1])
        pointer1 += 1
    return result


def intersect_and(doc_id_list_1, doc_id_list_2):
    result=[]
    pointer1=0
    pointer2=0
    while pointer1<len(doc_id_list_1) and pointer2<len(doc_id_list_2):
        if doc_id_list_1[pointer1]==doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1+=1
            pointer2+=1
        elif doc_id_list_1[pointer1]<doc_id_list_2[pointer2]:
            pointer1+=1
        else:
            pointer2+=1
    return result


def intersect_or(doc_id_list_1, doc_id_list_2):
    result=[]
    pointer1=0
    pointer2=0
    while pointer1<len(doc_id_list_1) and pointer2<len(doc_id_list_2):
        if doc_id_list_1[pointer1]==doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1+=1
            pointer2+=1
        elif doc_id_list_1[pointer1]<doc_id_list_2[pointer2]:
            result.append(doc_id_list_1[pointer1])
            pointer1+=1
        else:
            result.append(doc_id_list_2[pointer2])
            pointer2+=1
    while pointer1<len(doc_id_list_1):
        result.append(doc_id_list_1[pointer1])
        pointer1 += 1

    while pointer2<len(doc_id_list_2):
        result.append(doc_id_list_2[pointer2])
        pointer2 += 1

    return result






def get_doc_id(word_query, inverted_index):
    word_dictionary_string = inverted_index_word_retrival(word_query, inverted_index)
    if word_dictionary_string==-1:
        print(f"No documents found containing {word_query} ")
        return -1

    word_dictionary_string = word_dictionary_string.replace('},', '};')
    word_dictionary_string = word_dictionary_string.replace('[', '')
    word_dictionary_string = word_dictionary_string.replace(']', '')
    word_dictionary_string = word_dictionary_string.split(';')
    doc_id_list = []
    for dictionary_entry in word_dictionary_string:
        dictionary_entry = dictionary_entry.replace(' {', '{')
        dictionary_entry = ast.literal_eval(dictionary_entry)
        doc_id_list.append(dictionary_entry.get('doc_id'))

    return doc_id_list


def inverted_index_word_retrival(word, inverted_index):
    """


    Since the query_list and the index are both sorted alphabetically the search and retrieve
    takes O(n).

    :param bigraph_query_list: List of bigraph to be searched for
    :param index: The index to be searched
    :return: List of resulting words associated with the bigraph
    """
    #word.sort()
    data = pd.read_csv(inverted_index)
    point = 0
    result_list = []
    for xxxx in range(0, data.shape[0]):
        if data.iloc[xxxx, 0] == word:
            return data.iloc[xxxx, 2]

        elif str(data.iloc[xxxx + 1, 0]) > word:
            return -1
    return -1


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
            else:
                elements=elements[0]
        print(f'Element: {elements}')
        print(f' Output list: {output_list}')
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

    


if __name__ == '__main__':
    main()
