"""Build a dictionary of terms and index them."""

import pandas as pd

def build_it(corpus_filename: str,
             remove_stopwords=True, do_stemming=True, do_normalize=True):
    """Build a dictionary from the pre-processed corpus."""
    # Default to all word treatments on
    return ['test', 'computer', 'optimize']


def create_index(dictionary: str):
    """Associate dictionary terms to documents."""
    """Create a file with a set of doc ids and weight for each term"""

def find_in_index(query):
    queryList=query.split(", ")
    print(queryList)
    queryList.sort()
    data = pd.read_csv("inverted_index.csv")
    point=0
    for x in range(0, data.shape[0]):
        if data.iloc[x,0]==queryList[point]:
            print(data.iloc[x])
            point+=1
        elif str(data.iloc[x+1,0])>queryList[point]:
            print("Word not found")
            point+=1
        if point==len(queryList):
            break

def main():
    find_in_index("year")
    find_in_index("hash")
    find_in_index("hash, year")
    find_in_index("year, hash")






if __name__ == '__main__':
        main()