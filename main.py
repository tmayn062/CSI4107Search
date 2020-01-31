"""Search Engine Project for CSI4107."""
import gui
import corpus_preprocessing
import build_dictionary_and_index
import query
import spelling
HTMLFILE="UofO_Courses.html"
CORPUSUOTTAWA="corpus.xml"
INVETEDINDEXUOTTAWA="inverted_index.csv"

def main():
    """Run search engine and related functions."""
    # TODO : Update to include Reuters parse routine when available
    # remove_stopwords = True
    # do_stemming = True
    # do_normalize = True
    lingquistic_process_toggle = {"do_contractions": True, "do_normalize_hyphens": True,
                                  "do_normalize_periods": True, "do_remove_punctuation": True, "do_case_fold": True,
                                  "do_stop_word_removal": True, "do_stemming": True, "do_lemming": False}

    corpus_preprocessing.parse("UofO_Courses.html", "corpus.xml")
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
    gui.SearchEngineGUI()


if __name__ == '__main__':
    main()
