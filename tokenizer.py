import os
import re
import xml.etree.ElementTree as xml
from nltk.corpus import stopwords
import linguisticProcessor

import nltk
nltk.download('stopwords')
import string


def main():
    xmlFilename="uOttawaCourseList.xml"
    tree = xml.parse(xmlFilename)
    root = tree.getroot()
    stop_words = set(stopwords.words('english'))

    # for course in root:
    #     rawText=expand_contractions(course[2].text)

    # description_string=root[0][2].text
    # print(description_string)
    #
    # print(description_string
    test= "(U.S.A) state-of-the-art % % a the a on do not U.S.A, he.lp!!!!! don't won't I'm"

    print("+++++++++++++++++++++++")
    print(linguisticProcessor.linguisticModule(test))


    for coures in root:
        print(coures[0].text)
        print(linguisticProcessor.linguisticModule(coures[2].text))
        print("====================================================")



















if __name__ == '__main__':
    main()