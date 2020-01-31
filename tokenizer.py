import os
import re
import xml.etree.ElementTree as xml
from nltk.corpus import stopwords
import linguistic_processor
from linguistic_processor import linguistic_module
import pandas as pd
import nltk

nltk.download('stopwords')
import string
import csv


def main():
    xmlFilename = "uOttawaCourseList.xml"
    tree = xml.parse(xmlFilename)
    root = tree.getroot()
    stop_words = set(stopwords.words('english'))

    # for course_html_div_element in root:
    #     rawText=expand_contractions(course_html_div_element[2].text)

    # description_string=root[0][2].text
    # print(description_string)
    #
    # print(description_string
    test = "(U.S.A) state-of-the-art % % a the a on do not U.S.A, he.lp!!!!! don't won't I'm"

    print("+++++++++++++++++++++++")
    # print(linguisticProcessor.linguisticModule(test))

    lingquisticControl = {"contractions": True,  "Normalize Hyphens": True,
                          "Normalize Periods": True, "Punctuation": True, "Case Fold": True,
                          "stop word": True, "stemming": True, "lemming": False}
    countdd = 0
    completeList = []
    for coures in root:
        id = coures[0].text
        # print(course_id)

        text = linguisticModule(coures[2].text, lingquisticControl)
        # print(text)
        for words in text:
            wordTag = [id, words]

            tag = {"course_id": id, "word": words}
            completeList.append(tag)
        countdd += 1

    sortedList = sorted(completeList, key=lambda i: i['word'])
    prevCourseID = ""
    prevWord = ""
    docFrequency = 0
    termFrequency = 0
    idList = []
    invertedIndex = []
    for element in sortedList:
        courseID = element.get("course_id")
        word = element.get("word")

        if word == prevWord:
            if prevCourseID != courseID:
                docFrequency += 1
                termFrequency += 1
                idList.append(courseID)
                prevWord = word
                prevCourseID = courseID
            else:
                termFrequency += 1
                prevWord = word
                prevCourseID = courseID
        else:
            indexEntry = {"word": prevWord, "docFre": docFrequency, "termFre": termFrequency,
                          "postings": idList}
            invertedIndex.append(indexEntry)
            docFrequency = 1
            termFrequency = 1
            idList = [courseID]
            prevWord = word
            prevCourseID = courseID

    countd = 0
    countt = 0
    csvCreator()
    for element in invertedIndex:
        to_append = f'{element.get("word")};!{element.get("docFre")}' \
                    f';!{element.get("termFre")};!{element.get("postings")}'
        file = open("inverted_index.csv", 'a', newline='', encoding='utf-8')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split(';!'))
    data = pd.read_csv("inverted_index.csv")


def csvCreator():
    filename = "inverted_index.csv"
    os.unlink(filename)
    file = open(filename, 'w', newline='', encoding='utf-8')
    with file:
        header = ["Word", "Document Frequency", "Term Frequency", "Postings"]
        writer = csv.writer(file)
        writer.writerow(header)


if __name__ == '__main__':
    main()
