"""
Title: Dictionary and Inverted Index Builder Module

Project: CSI4107 Project
Version: Vanilla System
Component: Module 3 & 4

Created: 30 Jan 2020
Last modified: 31 Jan 2020

Author: Jonathan Boerger
Status: Complete

Description: This takes a corpus, applies linguistic processing on the documents within the corpus
            and creates an IR dictionary which is then used to build an inverted index in csv file
            format.

"""
import csv
import os
import xml.etree.ElementTree as xml
import pandas as pd
from linguistic_processor import linguistic_module


def __build_dictionary(corpus_filename, linguistic_processing_parameters):
    """
    This private method transform a corpus of documents into an IR dictionary. The documents undergo
    linguistic pre-processing prior to forming the dictionary.

    :param corpus_filename: Name of the corpus
    :param linguistic_processing_parameters: Dictionary (data struct.) specifying which linguistic
        process to apply to the text; see linguistic_processor.linguistic_module() for exact format
    :return: IR dictionary containing all words in the corpus associated with their
            respective document
    """
    dictionary = []
    tree = xml.parse(corpus_filename)
    root = tree.getroot()
    for course in root:
        doc_id = int(course.get('doc_id'))
        course_id = course[0].text
        processed_text = linguistic_module(course[2].text, linguistic_processing_parameters)

        for words in processed_text:
            tag = {"course_id": course_id, "doc_id": doc_id, "word": words}
            dictionary.append(tag)
    return dictionary


def __create_inverted_index(dictionary):
    """
    This private method takes an IR dictionary and creates an inverted index which includes document
    frequency and term frequency

    :param dictionary: List of dictionaries (data structure) containing word-docID association
    :return: Inverted index as a list of dictionaries (data structure)
    """
    # sorting dictionary on the value of the words
    sorted_dictionary = sorted(dictionary, key=lambda i: i['word'])

    # starting conditions
    previous_course_id = ""
    previous_word = ""
    previous_doc_id = 0
    term_frequency = 1
    document_frequency = 0
    term_frequency = 0
    posting_list = []
    inverted_index = []
    semaphore_one = 0
    semaphore_two = 0
    for element_index, element in enumerate(sorted_dictionary):
        doc_id = element.get("doc_id")
        course_id = element.get("course_id")
        word = element.get("word")

        # No change in word -> no entry in inverted index
        if word == previous_word:
            semaphore_one = 0

            # different docID -> add to posting list & increment document frequency
            if previous_course_id != course_id:

                document_frequency += 1
                posting_list.append({"course_id": previous_course_id, "doc_id": previous_doc_id,
                                     "term_frequency": term_frequency})
                previous_word = word
                previous_doc_id = doc_id
                previous_course_id = course_id
                term_frequency = 1
                semaphore_one = 1
                semaphore_two = 0
            # same docID -> carry on to next entry in dictionary
            else:
                term_frequency += 1
                previous_word = word
                previous_course_id = course_id
                previous_doc_id = doc_id
        # change in word -> add previous word to inverted index
        else:
            if semaphore_one == 1 or semaphore_two == 1:
                posting_list.append({"course_id": previous_course_id, "doc_id": previous_doc_id,
                                     "term_frequency": term_frequency})

            index_entry = {"word": previous_word, "document_frequency": document_frequency,
                           "postings": posting_list}
            inverted_index.append(index_entry)
            # setting up initial conditions for new word
            document_frequency = 1
            posting_list = [{"course_id": course_id, "doc_id": doc_id,
                             "term_frequency": term_frequency}]
            term_frequency = 1
            previous_word = word
            previous_course_id = course_id
            previous_doc_id = doc_id
            next_element = sorted_dictionary[element_index + 1]
            semaphore_one = 0
            semaphore_two = 0
            if next_element.get("word") == word:
                semaphore_two = 1
                posting_list = []

    return inverted_index


def __inverted_index_csv(inverted_index, inverted_index_filename):
    """
    This private methods creates a csv file for the inverted index and fills it

    :param inverted_index: The inverted index (in list form)
    :param inverted_index_filename: The name of the inverted index csv file
    :return: A csv file containing the inverted index
    """
    __inverted_index_csv_creator(inverted_index_filename)
    for element in inverted_index:
        to_append = f'{element.get("word")};!{element.get("document_frequency")}' \
                    f';!{element.get("postings")}'
        file = open(inverted_index_filename, 'a', newline='', encoding='utf-8')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split(';!'))


def __inverted_index_csv_creator(ii_filename):
    """
    This private methods creates a csv which will be used to store the inverted index.

    :ii_filename: file name for the csv file
    :return: an empty csv file
    """
    # since this method may be called when the csv file needs to be re-created
    # the methods deletes the existing
    try:
        os.unlink(ii_filename)
    except:
        pass
    file = open(ii_filename, 'w', newline='', encoding='utf-8')
    with file:
        header = ["Word", "Document Frequency", "Postings"]
        writer = csv.writer(file)
        writer.writerow(header)


def __linguistic_processing_parameter_csv_creator(lpp_file):
    """
    This private methods creates a csv which will be used to store the linguistic processing
    parameter information

    :param lpp_file: file name for the csv file
    :return: an empty csv file
    """
    # since this method may be called when the csv file needs to be re-created
    # the methods deletes the existing
    try:
        os.unlink(lpp_file)
    except:
        pass
    file = open(lpp_file, 'w', newline='', encoding='utf-8')
    with file:
        header = ["Para1", "Para2", "Para3", "Para4", "Para5", "Para6", "Para7", "Para8", ]
        writer = csv.writer(file)
        writer.writerow(header)


def __linguistic_processing_parameters_csv(linguistic_processing_parameters_dictionary,
                                           lpp_csv_file):
    """
    This private method creates and fills a csv file with the linguistic processing parameters

    :param linguistic_processing_parameters_dictionary: The dictionary (data structure) containing
    the LPP
    :param lpp_csv_file: the LPP csv file
    :return: a csv file containing LPP info
    """
    __linguistic_processing_parameter_csv_creator(lpp_csv_file)
    to_append = ''
    for key in linguistic_processing_parameters_dictionary:
        to_append = to_append + f' {linguistic_processing_parameters_dictionary[key]}'
    file = open(lpp_csv_file, 'a', newline='', encoding='utf-8')
    with file:
        writer = csv.writer(file)
        writer.writerow(to_append.split())


def __linguistic_processor_parameters_validator(lpp_csv_file, lpp_dictionary):
    """
    This private method compared the inverted index LPP to the currently specified LPP
    for any differences

    :param lpp_csv_file: the csv file containing the LPP for the current inverted index csv
    :param lpp_dictionary: a dictionary (data structure) containing the current LPP
    :return: -1 if there is a differnece between the LPP found in the csv file and those
                specific in the dictionary
            1 if the csv file and dictionary match
    """
    previous_lingguistic_settings = []
    current_lingguistic_settings = []
    data = pd.read_csv(lpp_csv_file)
    for index in range(0, 8):
        previous_lingguistic_settings.append(data.iloc[0, index])
    for key in lpp_dictionary:
        current_lingguistic_settings.append(lpp_dictionary[key])
    for index in range(0, 8):
        if current_lingguistic_settings[index] == previous_lingguistic_settings[index]:
            pass
        else:
            return -1
    return 1


def dictionary_and_inverted_index_wrapper(linguistic_control_dictionary, inverted_index_filename,
                                          corpus_filename, lp_parameter_filename):
    """
    This is the public methods for the build dictionary and inverted index module.
    This methods integrates all methods required to build the IR dictionary and its
    corresponding inverted index.
    Additionally, it also checks to see if the inverted file already exist, if it does
    the methods carries on without recreating the index.
    Lastly, in the event that the linguistic pre-processing parameters are changed, regardless
    if the inverted index already exist, will create a new inverted index to reflect
    the changes in dictionary resulting from different linguistic processing.



    :param linguistic_control_dictionary: The dictionary which specifies which linguistic
        processing modules should be used to create the inverted index.
    :param inverted_index_filename: The inverted index file name
     :param corpus_filename:
    :param lp_parameter_filename: The linguistic processing control file
    :return: A csv file containing the inverted index
    """

    def create_index():
        ir_dictionary = __build_dictionary(corpus_filename, linguistic_control_dictionary)
        inverted_index = __create_inverted_index(ir_dictionary)
        __inverted_index_csv(inverted_index, inverted_index_filename)
        __linguistic_processing_parameters_csv(linguistic_control_dictionary, lp_parameter_filename)

    # The required files dont exits -> create them
    if not os.path.exists(inverted_index_filename)  \
            or not os.path.exists(lp_parameter_filename):
        print("Not all files exist which need to exist thus we are creating them")
        create_index()
        return

    check_val = __linguistic_processor_parameters_validator(lp_parameter_filename,
                                                            linguistic_control_dictionary)
    # the required files exist & no changes to the LPP -> carry on
    if check_val == -1:
        print("II already exits, however there has been a change in LP settings, thus "
              "recalculating it")
        create_index()

    # the required files exist BUT changes to the LPP -> create a new inverted index
    else:
        print("II already exist and there has been no change in LP settings. Therefore all done.")

    return
