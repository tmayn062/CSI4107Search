"""Configuration info."""
UOTTAWA = "uOttawa"
REUTERS = "Reuters"
CORPUS = dict()
CORPUS[UOTTAWA] = {"source" : "UofO_Courses.html",
                   "corpusxml" : "uottawa_corpus.xml",
                   "inverted_index_file" : "uottawa_inverted_index.csv",
                   "vsm_inverted_index_file" : "uottawa_vsm_inverted_index.csv",
                   "lpp_file" : "uottawa_lpp.csv",
                   "bigraph_file" : "uottawa_bigraph_index.csv",
                   "spelling_file" : "uottawa_spelling.csv"}
CORPUS[REUTERS] = {"source" : "UofO_Courses.html",
                   "corpusxml" : "reuters_corpus.xml",
                   "inverted_index_file" : "reuters_inverted_index.csv",
                   "vsm_inverted_index_file" : "reuters_vsm_inverted_index.csv",
                   "lpp_file" : "reuters_lpp.csv",
                   "bigraph_file" : "reuters_bigraph_index.csv",
                   "spelling_file" : "reuters_spelling.csv"}

#HTML_FILE = "UofO_Courses.html"

#UOTTAWA_CORPUS = "uottawa_corpus.xml"
#REUTERS_CORPUS = "reuters_corpus.xml"
#UOTTAWA_INVERTED_INDEX = "uottawa_inverted_index.csv"
#REUTERS_INVERTED_INDEX = "reuters_inverted_index.csv"
#UOTTAWA_VSM_INVERTED_INDEX = "uottawa_vsm_inverted_index.csv"
#REUTERS_VSM_INVERTED_INDEX = "reuters_vsm_inverted_index.csv"
#UOTTAWA_LPP = "uottawa_lpp.csv"
#REUTERS_LPP = "reuters_lpp.csv"
#UOTTAWA_BIGRAPH = "uottawa_bigraph_index.csv"
#REUTERS_BIGRAPH = "reuters_bigraph_index.csv"
K_RETRIEVAL = 10
LINGUISTIC_PARAMS = {"do_contractions": True,
                     "do_normalize_hyphens": True,
                     "do_normalize_periods": True,
                     "do_remove_punctuation": True,
                     "do_case_fold": True,
                     "do_stop_word_removal": True,
                     "do_stemming": True,
                     "do_lemming": False}
