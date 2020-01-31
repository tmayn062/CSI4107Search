import os
import re
import xml.etree.ElementTree as xml
from nltk.corpus import stopwords
from contractions import expand_contractions
import string
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')


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

def stemmer(rawTextList):
    porter = PorterStemmer()
    results=[]
    for words in rawTextList:
        results.append(porter.stem(words))
    return results

def lemmatizer(rawTextList):
    lemmatizer = WordNetLemmatizer()
    results=[]
    for words in rawTextList:
        results.append(lemmatizer.lemmatize(words))
    return results


def linguisticModule(rawText, controlList):
    if type(controlList)== list:
        if controlList[0]==1:
            cleanText=contractionsCleanser(rawText)
        if controlList[1] == 1:
            cleanText=tokenize(cleanText)
        if controlList[2] == 1:
            cleanText=normalizerHyphens(cleanText)
        if controlList[3] == 1:
            cleanText=normalizerPeriods(cleanText)
        if controlList[4] == 1:
            cleanText=punctionCleanser(cleanText)
        if controlList[5] == 1:
            cleanText=caseFold(cleanText)
        if controlList[6] == 1:
            cleanText=stopwordRemouval(cleanText)
        if controlList[7] == 1:
            cleanText=stemmer(cleanText)
        if controlList[8] == 1:
            cleanText=lemmatizer(cleanText)
    else:
        if controlList.get("contractions"):
            cleanText=contractionsCleanser(rawText)
        if controlList.get("tokenization"):
            cleanText=tokenize(cleanText)
        if controlList.get("Normalize Hyphens"):
            cleanText=normalizerHyphens(cleanText)
        if controlList.get("Normalize Periods"):
            cleanText=normalizerPeriods(cleanText)
        if controlList.get("Punctuation"):
            cleanText=punctionCleanser(cleanText)
        if controlList.get("Case Fold"):
            cleanText=caseFold(cleanText)
        if controlList.get("stop word"):
            cleanText=stopwordRemouval(cleanText)
        if controlList.get("stemming"):
            cleanText=stemmer(cleanText)
        if controlList.get("lemming"):
            cleanText=lemmatizer(cleanText)

    return cleanText


