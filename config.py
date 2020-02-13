"""Configuration info."""
UOTTAWA = "uOttawa"
REUTERS = "Reuters"
CORPUS = dict()
CORPUS[UOTTAWA] = {"source" : "UofO_Courses.html",
                   "corpusxml" : "uottawa_corpus.xml",
                   "inverted_index_file" : "uottawa_inverted_index.csv",
                   "lpp_file" : "uottawa_lpp.csv",
                   "bigraph_file" : "uottawa_bigraph_index.csv",
                   "spelling_file" : "uottawa_spelling.csv"}
CORPUS[REUTERS] = {"source" : "UofO_Courses.html",
                   "corpusxml" : "reuters_corpus.xml",
                   "inverted_index_file" : "reuters_inverted_index.csv",
                   "lpp_file" : "reuters_lpp.csv",
                   "bigraph_file" : "reuters_bigraph_index.csv",
                   "spelling_file" : "reuters_spelling.csv"}


K_RETRIEVAL = 20
TOP_N_SPELLING = 3
LINGUISTIC_PARAMS = {"do_contractions": True,
                     "do_normalize_hyphens": True,
                     "do_normalize_periods": True,
                     "do_remove_punctuation": True,
                     "do_case_fold": True,
                     "do_stop_word_removal": True,
                     "do_stemming": True,
                     "do_lemming": False}
