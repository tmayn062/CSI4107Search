"""Apply stemming, stopword removal, and normalization to text."""
# Adapted from code in https://www.analyticsvidhya.com/blog/2019/08
# /how-to-remove-stopwords-text-normalization-nltk-spacy-gensim-python/
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def tokenize(words):
    """Tokenize text for preprocessing."""
    return word_tokenize(words)


def remove_stopwords(word_tokens):
    """Remove stopwords from the given list of word tokens."""
    stop_words = set(stopwords.words('english'))
    filtered_text = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_text.append(w)
    return filtered_text


def stem_text(word_tokens):
    """Apply stemming to the given list of word tokens."""
    stemmed_text = []
    ps = PorterStemmer()
    for w in word_tokens:
        stemmed_text.append(ps.stem(w))
    return stemmed_text


def normalize(word_tokens):
    """Normalize the list of words by removing period and hyphen."""
    normalized_text = []
    for w in word_tokens:
        normalized_text.append(w.replace('.', '').replace('-', ''))
    return normalized_text
