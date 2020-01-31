"""
Title: Dictionary and Inverted Index Builder Module

Project: CSI4107 Project
Version: Vanilla System
Component: Module 3 & 4

Created: 30 Jan 2020
Last modified: 31 Jan 2020

Author: Jonathan Boerger
Status: In progress

Description: This takes a corpus, applies linguistic processing on the documents within the corpus
            and creates an IR dictionary which is then used to build an inverted index in csv file
            format.

"""
import xml.etree.ElementTree as xml
import pandas as pd
from linguistic_processor import linguistic_module


def build_dictionary(corpus_filename, linquistic_toggole):
    """

    :param corpus_filename: Name of the corpus
    :param linquistic_toggole: Dictionary (data structure) specifying which linguistic process to
        apply to the text; see linguistic_processor.linguistic_module() for exact format
    :return: IR dictionary containing all words in the corpus associated with their
            respective document
    """
    dictionary = []
    tree = xml.parse(corpus_filename)
    root = tree.getroot()
    for course in root:
        course_id = course[0].text
        processed_text = linguistic_module(course[2].text, linquistic_toggole)

        for words in processed_text:
            tag = {"course_id": course_id, "word": words}
            dictionary.append(tag)
    return dictionary


def create_inverted_index(dictionary):
    """
    This method takes an IR dictionary and creates an inverted index

    :param dictionary: List of dictionaries (data structure) containing word-docID association
    :return: Inverted index as a list of dictionaries (data structure)
    """
    # sorting dictionary on the value of the words
    sorted_dictionary = sorted(dictionary, key=lambda i: i['word'])

    # starting conditions
    previous_course_id = ""
    previous_word = ""
    document_frequency = 0
    posting_list = []
    inverted_index = []

    for element in sorted_dictionary:
        course_id = element.get("course_id")
        word = element.get("word")

        # No change in word -> no entry in inverted index
        if word == previous_word:
            # different docID -> add to posting list & increment document frequency
            if previous_course_id != course_id:
                document_frequency += 1
                posting_list.append(course_id)
                previous_word = word
                previous_course_id = course_id
            # same docID -> carry on to next entry in dictionary
            else:
                previous_word = word
                previous_course_id = course_id
        # change in word -> add previous word to inverted index
        else:
            index_entry = {"word": previous_word, "document_frequency": document_frequency,
                          "postings": posting_list}
            inverted_index.append(index_entry)
            # setting up initial conditions for new word
            document_frequency = 1
            posting_list = [course_id]
            previous_word = word
            previous_course_id = course_id
    return inverted_index


def find_in_index(query):
    queryList = query.split(", ")
    print(queryList)
    queryList.sort()
    data = pd.read_csv("inverted_index.csv")
    point = 0
    for x in range(0, data.shape[0]):
        if data.iloc[x, 0] == queryList[point]:
            print(data.iloc[x])
            point += 1
        elif str(data.iloc[x + 1, 0]) > queryList[point]:
            print("Word not found")
            point += 1
        if point == len(queryList):
            break


def main():
    find_in_index("year")
    find_in_index("hash")
    find_in_index("hash, year")
    find_in_index("year, hash")


if __name__ == '__main__':
    main()
