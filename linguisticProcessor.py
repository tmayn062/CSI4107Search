import os
import re
import xml.etree.ElementTree as xml
from nltk.corpus import stopwords
from contractions import expand_contractions
import string


def stopwordRemouval(rawTextList):
    filtered_sentence = []
    stop_words = set(stopwords.words('english'))

    for w in rawTextList:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

def contractionsCleanser(rawText):
    return expand_contractions(rawText)

def normalizerPeriods(rawTextList):
    results = []
    for words in rawTextList:
        if words.find('.') != -1:
            words= words.replace('.', '')
        results.append(words)
    return results

def normalizerHyphens(rawTextList):
    results=[]
    for words in rawTextList:
        if words.find('-') != -1:
            temp = words.replace('-', ' ')
            hyphenProduct = temp.split()
            for word in hyphenProduct:
                results.append(word)
        else:
            results.append(words)
    return results

def caseFold(rawTextList):
    lowerCaseWords=[w.lower() for w in rawTextList]
    return lowerCaseWords

def punctionCleanser(rawTextList):
    # from https://machinelearningmastery.com/clean-text-machine-learning-python/
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in rawTextList]
    result=[]
    for words in stripped:
        if words=="":
            pass
        else:
            result.append(words)
    return result

def tokenize(rawText):
    words=rawText.split()
    return words

def linguisticModule(rawText):
    cleanText=contractionsCleanser(rawText)
    cleanText=tokenize(cleanText)
    cleanText=normalizerHyphens(cleanText)
    cleanText=normalizerPeriods(cleanText)
    cleanText=punctionCleanser(cleanText)
    cleanText=caseFold(cleanText)
    cleanText=stopwordRemouval(cleanText)
    return cleanText

