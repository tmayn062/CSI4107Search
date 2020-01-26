"""Search Engine Project for CSI4107."""
import gui
import corpus_preprocessing
import build_dictionary_and_index


def main():
    """Run search engine and related functions."""
    # TODO : Update to include Reuters parse routine when available
    corpus_preprocessing.parse("UofO_Courses.html")
    # TODO : Update to include Reuters dictionary routine when available
    build_dictionary_and_index.build_it("uOttawaCourseList.xml",
                                        remove_stopwords=True,
                                        do_stemming=True,
                                        do_normalize=True)
    gui.SearchEngineGUI()


main()
