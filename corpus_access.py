"""
Access corpus of documents

Project: CSI4107 Project
Version: Vanilla System
Component: Module 5

Created: 26 Jan 2020
Last modified: 09 Feb 2020

Author: Tiffany Maynard
Status: Completed

Description: Access documents from the corpus

"""
import xml.etree.ElementTree as xml
import os.path
from dataclasses import dataclass
import config

@dataclass
class Document:
    """Document holds all the document info from a corpus."""
    doc_id: int
    title: str
    doctext: str


def get_documents(corpus, list_doc_ids):
    """Return a list of documents using a given list of doc ids
       order of doc ids is preserved."""
    # XML parse code adapted from
    # https://stackabuse.com/reading-and-writing-xml-files-in-python/
    corpus_filename = config.CORPUS[corpus]['corpusxml']
    if not os.path.isfile(corpus_filename):
        print(corpus_filename + ' does not exist')
        return []
    tree = xml.parse(corpus_filename)
    root = tree.getroot()
    doc_list = []
    for i in list_doc_ids:
        doc_to_add = Document(i,
                              root[i][0].text+' '+root[i][1].text,
                              root[i][2].text)
        doc_list.append(doc_to_add)
    return doc_list
