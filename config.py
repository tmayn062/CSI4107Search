"""Configuration info."""
UOTTAWA = "uOttawa"
REUTERS = "Reuters"
CORPUS = dict()
CORPUS[UOTTAWA] = {"source" : "UofO_Courses.html",
                   "corpusxml" : "uottawa_corpus.xml",
                   "inverted_index_file" : "uottawa_inverted_index.csv",
                   "lpp_file" : "uottawa_lpp.csv",
                   "bigraph_file" : "uottawa_bigraph_index.csv",
                   "spelling_file" : "uottawa_spelling.csv",
                   "relevance_file" : "uottawa_relevance.csv"}
CORPUS[REUTERS] = {"source" : "/home/tjm/Documents/Winter2020/CSI4107/reuters21578",
                   "corpusxml" : "reuters_corpus.xml",
                   "inverted_index_file" : "reuters_inverted_index.csv",
                   "lpp_file" : "reuters_lpp.csv",
                   "bigraph_file" : "reuters_bigraph_index.csv",
                   "spelling_file" : "reuters_spelling.csv",
                   "relevance_file" : "reuters_relevance.csv"}


K_RETRIEVAL = 20
TOP_N_SPELLING = 3
EXPANSION_SYNONYMS = 5
MAX_EXPAND_QUERY_LEN = 3
LINGUISTIC_PARAMS = {"do_contractions": True,
                     "do_normalize_hyphens": True,
                     "do_normalize_periods": True,
                     "do_remove_punctuation": True,
                     "do_case_fold": True,
                     "do_stop_word_removal": True,
                     "do_stemming": True,
                     "do_lemming": False}
ROCCHIO_ALPHA = 1
ROCCHIO_BETA = 0.75
ROCCHIO_GAMMA = 0.15
ROCCHIO_MIN = 0.1
TOPICS = ['acq', 'alum', 'barley', 'bop', 'carcass', 'castor-oil', 'cocoa', 'coconut',
          'coconut-oil', 'coffee', 'copper', 'copra-cake', 'corn', 'cotton', 'cotton-oil', 'cpi',
          'cpu', 'crude', 'dfl', 'dlr', 'dmk', 'earn', 'fuel', 'gas', 'gnp', 'gold', 'grain',
          'groundnut', 'groundnut-oil', 'heat', 'hog', 'housing', 'income', 'instal-debt',
          'interest', 'ipi', 'iron-steel', 'jet', 'jobs', 'l-cattle', 'lead', 'lei', 'lin-oil',
          'livestock', 'lumber', 'meal-feed', 'money-fx', 'money-supply', 'naphtha', 'nat-gas',
          'nickel', 'nkr', 'nzdlr', 'oat', 'oilseed', 'orange', 'palladium', 'palm-oil',
          'palmkernel', 'pet-chem', 'platinum', 'potato', 'propane', 'rand', 'rape-oil',
          'rapeseed', 'reserves', 'retail', 'rice', 'rubber', 'rye', 'ship', 'silver',
          'sorghum', 'soy-meal', 'soy-oil', 'soybean', 'strategic-metal', 'sugar', 'sun-meal',
          'sun-oil', 'sunseed', 'tea', 'tin', 'trade', 'veg-oil', 'wheat', 'wpi', 'yen', 'zinc']
