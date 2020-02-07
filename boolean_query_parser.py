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

"""
 Next steps:
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
    test_string=wildcard_word_finder('*ge', "uottawa_bigraph_index.csv")
    test_string=test_string.replace('(', '( ')
    test_string =test_string.replace(')', ' )')
    test_string=test_string.split()
    operators=["AND","OR","NOT_AND"]
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
