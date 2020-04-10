"""
Title: Reuters Pre-processing Module

Project: CSI4107 Project
Version: Final System
Component: Module 2 (Vanilla)

Created: 10 Apr 2020
Last modified: 10 Apr 2020

Author: Tiffany Maynard
Status: In Progress

Description: This module takes Reuters corpus and extracts information to create
an XML document corpus.
Adapted from https://miguelmalvarez.com/2015/03/20/classifying-reuters-21578-collection-with-python-representing-the-data/
"""
import os
import glob
import bs4
import xml.etree.ElementTree as xml
from nltk.corpus import reuters
import config

def print_info():
    documents = reuters.fileids()
    print(str(len(documents)) + " documents")
    print(reuters.categories())
    category_docs = reuters.fileids("rubber")
    document_id = category_docs[0]
    document_words = reuters.words(category_docs[0])


    # Raw document
    print(reuters.raw(document_id))



def xml_writer(doclist, filename):
    """
    This methods takes a list of document info
    and adds it to the XML corpus.
        :param doclist: list of document info
        :param filename: Name of XML corpus

    """
    root = xml.Element("Articles")
    with open(filename, "wb") as f:
        for doc in doclist:
            user_element = xml.Element("Article")
            user_element.set("doc_id", doc[0])
            root.append(user_element)
            doc_id = xml.SubElement(user_element, "doc_id")
            doc_id.text = doc[0]
            title = xml.SubElement(user_element, "title")
            title.text = doc[1]
            body = xml.SubElement(user_element, "body")
            body.text = doc[2]
            topics = xml.SubElement(user_element, "topics")
            topics.text = doc[3]
        tree = xml.ElementTree(root)
        tree.write(f)

def create_reuters_corpus():
    """read in sgm files and create a corpus in XML"""
    #adapted from
    #https://medium.com/@namanjain2050/
    #finding-similar-documents-reuters-dataset-example-part-4-eb0462e1ab2b
    documents = []
    corpus_filename = config.CORPUS[config.REUTERS]['corpusxml']
    if os.path.exists(corpus_filename) is True:
        if os.path.getsize(corpus_filename) > 0:
            print("Reuters corpus already exists")
            return
    path = '/home/tjm/Documents/Winter2020/CSI4107/reuters21578'
    for filename in glob.glob(os.path.join(path, '*.sgm')):
        with open(filename, 'rb') as f:
            data = f.read()
            soup = bs4.BeautifulSoup(data, 'html.parser')
            docs = soup.findAll("reuters")
#            contents = soup.findAll('body')
            for doc in docs:
                doc_attrs = doc.attrs
                title = ""
                body = ""
                topics = ""
                if doc.find("body"):
                    body = doc.find("body").text.replace('\n', ' ').replace('\r', '')
                    body = body.replace('\x03', '')
                if doc.find("title"):
                    title = doc.find("title").text
                if doc.find("topics"):
                    for topic in doc.find("topics"):
                        topics += topic.text + ' '
                documents.append([doc_attrs['newid'], title,
                                  body, topics])
#            for content in contents:
#               documents.append(content.text)

    xml_writer(documents, corpus_filename)
