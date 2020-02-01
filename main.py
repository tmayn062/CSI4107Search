"""Search Engine Project for CSI4107."""
import gui
import corpus_preprocessing
import build_dictionary_and_index
import query
import spelling
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
from linguistic_processor import linguistic_module
from datetime import datetime
html_file="UofO_Courses.html"
uottawa_corpus="uottawa_corpus.xml"
uottawa_inverted_index="uottawa_inverted_index.csv"
uottawa_lpp="uottawa_lpp.csv"


def main():
    """Run search engine and related functions."""
    # TODO : Update to include Reuters parse routine when available
    # remove_stopwords = True
    # do_stemming = True
    # do_normalize = True
    start_time=datetime.now()
    print(datetime.now())
    linguistic_processing_parameters = {"do_contractions": True, "do_normalize_hyphens": False,
                                        "do_normalize_periods": False, "do_remove_punctuation": True,
                                        "do_case_fold": True, "do_stop_word_removal": True,
                                        "do_stemming": True, "do_lemming": False}

    corpus_preprocessing.parse(html_file, uottawa_corpus)
    dictionary_and_inverted_index_wrapper(linguistic_processing_parameters,uottawa_inverted_index,
                                          uottawa_corpus, uottawa_lpp)
    end_time=datetime.now()
    total_time=end_time-start_time
    print(total_time)
    print(datetime.now())

    test_string = "U.S.A. hello. he.lp state-of-the-art"
    test_tokens=linguistic_module(test_string, linguistic_processing_parameters)
    for token in test_tokens:
        print(token)

    # TODO : Update to include Reuters dictionary routine when available
    # build_dictionary_and_index.build_it("uOttawaCourseList.xml",
    #                                     remove_stopwords,
    #                                     do_stemming,
    #                                     do_normalize)

    # print(query.process("testing U.S.A. low-cost women babies cacti ",
    #                     remove_stopwords,
    #                     do_stemming,
    #                     do_normalize))
    # print(spelling.edit_distance("execution", "intention"))
    # print(spelling.edit_distance("sunday", "saturday"))
    # print(spelling.edit_distance("dog", "do"))
    #gui.SearchEngineGUI()



# _____________________________________________________________---
# def find_in_index(query):
#     queryList = query.split(", ")
#     print(queryList)
#     queryList.sort()
#     data = pd.read_csv("inverted_index.csv")
#     point = 0
#     for x in range(0, data.shape[0]):
#         if data.iloc[x, 0] == queryList[point]:
#             print(data.iloc[x])
#             point += 1
#         elif str(data.iloc[x + 1, 0]) > queryList[point]:
#             print("Word not found")
#             point += 1
#         if point == len(queryList):
#             break

if __name__ == '__main__':
    main()
