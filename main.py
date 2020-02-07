"""Search Engine Project for CSI4107."""
import gui
import corpus_preprocessing
import build_dictionary_and_index
import query
import spelling
from wildcard_management import wildcard_word_finder
from build_dictionary_and_index import dictionary_and_inverted_index_wrapper
from linguistic_processor import linguistic_module
from datetime import datetime
import boolean
html_file="UofO_Courses.html"
uottawa_corpus="uottawa_corpus.xml"
uottawa_inverted_index="uottawa_inverted_index.csv"
uottawa_lpp="uottawa_lpp.csv"
uottawa_bigraph= "uottawa_bigraph_index.csv"


def main():
    """Run search engine and related functions."""
    # TODO : Update to include Reuters parse routine when available
    # remove_stopwords = True
    # do_stemming = True
    # do_normalize = True
    start_time=datetime.now()
    print(datetime.now())
    linguistic_processing_parameters = {"do_contractions": True, "do_normalize_hyphens": True,
                                        "do_normalize_periods": True, "do_remove_punctuation": True,
                                        "do_case_fold": True, "do_stop_word_removal": True,
                                        "do_stemming": True, "do_lemming": False}

    corpus_preprocessing.parse(html_file, uottawa_corpus)
    dictionary_and_inverted_index_wrapper(linguistic_processing_parameters,uottawa_inverted_index,
                                          uottawa_corpus, uottawa_lpp, uottawa_bigraph)
    end_time=datetime.now()
    total_time=end_time-start_time
    print(total_time)
    print(datetime.now())

    test_string = "U.S.A. hello. he.lp state-of-the-art"
    test_tokens=linguistic_module(test_string, linguistic_processing_parameters)
    for token in test_tokens:
        print(token)

    tesstt=linguistic_module('*ey',linguistic_processing_parameters)
    print(tesstt)

    print(wildcard_word_finder(tesstt[0], uottawa_bigraph))


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





if __name__ == '__main__':
    main()
