"""
Title:  Text Categorization with kNN

Project: CSI4107 Project
Version: Final System
Component: Module 6

Created: 10 Apr 2020
Last modified: 13 Apr 2020

Author: Tiffany Maynard
Status: In Progress

Description: Assign one or more topics to the Reuters documents that are not assigned any
topics
Based on https://miguelmalvarez.com/2015/03/20/classifying-reuters-21578-collection-with-python-representing-the-data/
"""
import csv
import os
import ast
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords, reuters
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
import bs4
import config
#Empty globals to store topics so it is only read once from csv
TOPIC_DICT = {}


def doc_id_by_topic():
    """create a dictionary of topics to list doc_ids by going through reuters corpus"""

    corpus_filename = config.CORPUS[config.REUTERS]['corpusxml']
    topic_dict = dict()
    all_doc_ids = []
    with open(corpus_filename, 'rb') as f:
        data = f.read()
        soup = bs4.BeautifulSoup(data, 'html.parser')
        articles = soup.findAll("article")
        for article in articles:
            doc_id = article.find("doc_id").text
            all_doc_ids.append(doc_id)
            topics = article.find("topics").text.strip().split(' ')
            #some articles have multiple topics
            for topic in topics:
                if topic in topic_dict:
                    doc_list = topic_dict.get(topic)
                    doc_list.append(doc_id)
                    topic_dict[topic] = doc_list
                else:
                    topic_dict[topic] = [doc_id]
    topic_dict['all-topics'] = list(set(all_doc_ids))
    topic_dict['notopic'] = topic_dict.pop('')
    write_topics_tocsv(topic_dict)

def write_topics_tocsv(topics):
    """write the topic file to csv"""
    csv_filename = config.CORPUS[config.REUTERS]['doc_by_topic']
    with open(csv_filename, 'w') as file:
        writer = csv.writer(file)
        for key, value in topics.items():
            writer.writerow([key, value])

def read_topics_from_csv():
    """Read in the csv file that stores the topic info for a corpus"""
    filename = config.CORPUS[config.REUTERS]['doc_by_topic']
    topic_dict = dict()
    if os.path.exists(filename):
        print('reading from topics csv')
        with open(filename, newline='') as data_file:
            reader = csv.reader(data_file)
            for row in reader:
                topic_dict[row[0]] = ast.literal_eval(row[1])
        return topic_dict

    return {}

def get_topic_dict():
    """Wrapper to avoid multiple dictionary reads from csv."""
    global TOPIC_DICT
    if TOPIC_DICT:
        return TOPIC_DICT
    TOPIC_DICT = read_topics_from_csv()
    return TOPIC_DICT

cachedStopWords = stopwords.words("english")

#code below is from
#https://miguelmalvarez.com/2015/03/20/classifying-reuters-21578-collection-with-python-representing-the-data/
def tokenize(text):
	min_length = 3
	words = map(lambda word: word.lower(), word_tokenize(text))
	words = [word for word in words
                  if word not in cachedStopWords]
	tokens =(list(map(lambda token: PorterStemmer().stem(token),
                  words)));
	p = re.compile('[a-zA-Z]+')
	filtered_tokens = list(filter(lambda token:
                  p.match(token) and len(token)>=min_length,tokens))
	return filtered_tokens

def tf_idf(docs):
	tfidf = TfidfVectorizer(tokenizer=tokenize, min_df=3,
                        max_df=0.90, max_features=3000,
                        use_idf=True, sublinear_tf=True,
                        norm='l2')
	tfidf.fit(docs)
	return tfidf

def feature_values(doc, representer):
	doc_representation = representer.transform([doc])
	features = representer.get_feature_names()
	return [(features[index], doc_representation[0, index])
                 for index in doc_representation.nonzero()[1]]

def main():
	train_docs = []
	test_docs = []

	for doc_id in reuters.fileids():
		if doc_id.startswith("train"):
			train_docs.append(reuters.raw(doc_id))
		else:
			test_docs.append(reuters.raw(doc_id))

	representer = tf_idf(train_docs);

	for doc in test_docs[:15]:
	    print(doc_id)
	    print(feature_values(doc, representer))

if __name__ == '__main__':
    main()
