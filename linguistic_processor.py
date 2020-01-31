"""
Linguistic Processor Module

CSI4107 Project
Vanilla System

Created: 30 Jan 2020
Last modified: 31 Jan 2020

@author: Jonathan Boeger

Status: Complete
"""

import string
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from contractions import expand_contractions

nltk.download('wordnet')


def stopword_remouval(raw_text_list):
    """
    This method removes all stop words, as defined in the NLTK package.

    :param raw_text_list: List of tokenized words strings
    :return: List of tokenized words with all stop words removed
    """
    filtered_sentence = []
    stop_words = set(stopwords.words('english'))

    for word in raw_text_list:
        if word not in stop_words:
            filtered_sentence.append(word)
    return filtered_sentence


def contractions_expander(raw_text):
    """
    This method is a wrapper method for DIP's 'expand_contraction' method. Source code is credited
    in contractions.py file.

    The method expands all contractions found in a string.

    :param raw_text: String of text
    :return: String of text where all contractions are expanded
    """
    return expand_contractions(raw_text)


def normalizer_periods(raw_text_list):
    """
    This method removes all periods from a list of strings.

    :param raw_text_list: List of tokenized words strings
    :return: List of tokenized word strings with periods removed
    """
    results = []
    for words in raw_text_list:
        if words.find('.') != -1:
            words = words.replace('.', '')
        results.append(words)
    return results


def normalizer_hyphens(raw_text_list):
    """
        This method splits all words that contains hyphens into its component words

        :param raw_text_list: List of tokenized words strings
        :return: List of tokenized word strings with hyphenated word replaced by its component words
    """
    results = []
    for words in raw_text_list:
        if words.find('-') != -1:
            # splitting hyphenated word and adding it to the result list
            temp = words.replace('-', ' ')
            hyphen_words = temp.split()
            for word in hyphen_words:
                results.append(word)
        else:
            results.append(words)
    return results


def case_fold(raw_text_list):
    """
    This method converts all letters in a string to lower case letters

    :param raw_text_list: List of tokenized words strings
    :return: List of tokenized words strings where all letters are lower case
    """
    lower_case_words = [w.lower() for w in raw_text_list]
    return lower_case_words


def punctuation_remover(raw_text_list):
    """
    This method removes all punctuation marks, as defined by python string, from a string

    This method is adapted from code online tutorial by Jason Brownlee found at
    https://machinelearningmastery.com/clean-text-machine-learning-python/

    :param raw_text_list: List of tokenized words strings
    :return: List of tokenized words strings where punctuations marks are removed.
    """

    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in raw_text_list]
    result = []
    for words in stripped:
        # removing any potential empty items ([""])
        if words == "":
            pass
        else:
            result.append(words)
    return result


def tokenize(raw_text):
    """
    This methods tokenize a string of text on whitespace

    :param raw_text: A string of text
    :return: A list containing individual string tokens
    """
    words = raw_text.split()
    return words


def stemmer(raw_text_list):
    """
    This methods applies the NLTK porter stemmer to a list of words

    :param raw_text_list: List of tokenized words strings
    :return: List of stemmed words strings
    """
    porter = PorterStemmer()
    results = []
    for words in raw_text_list:
        results.append(porter.stem(words))
    return results


def lemmatizer(raw_text_list):
    """
        This methods applies the NLTK Word Net lemmatizer to a list of words

        :param raw_text_list: List of tokenized words strings
        :return: List of lemmatized words strings
    """
    wordnet_lemmatizer = WordNetLemmatizer()
    results = []
    for words in raw_text_list:
        results.append(wordnet_lemmatizer.lemmatize(words))
    return results


def linguistic_module(raw_text, control_dic):
    """
    This method takes a string of text and applies specified linguistic text process.

    :param raw_text: A string of text
    :param control_dic: A dictionary in the form bellow, which is used to specify which
    linguistic processes to be applied to the raw text.
            {"contractions": True,  "Normalize Hyphens": True,
              "Normalize Periods": True, "Punctuation": True, "Case Fold": True,
              "stop word": True, "stemming": True, "lemming": False}

    :return: A list which contains fully processed tokens
    """
    if control_dic.get("contractions"):
        clean_text = contractions_expander(raw_text)

    clean_text = tokenize(clean_text)
    if control_dic.get("Normalize Hyphens"):
        clean_text = normalizer_hyphens(clean_text)
    if control_dic.get("Normalize Periods"):
        clean_text = normalizer_periods(clean_text)
    if control_dic.get("Punctuation"):
        clean_text = punctuation_remover(clean_text)
    if control_dic.get("Case Fold"):
        clean_text = case_fold(clean_text)
    if control_dic.get("stop word"):
        clean_text = stopword_remouval(clean_text)
    if control_dic.get("stemming"):
        clean_text = stemmer(clean_text)
    if control_dic.get("lemming"):
        clean_text = lemmatizer(clean_text)

    return clean_text
