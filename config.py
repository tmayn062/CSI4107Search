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
                   "relevance_file" : "uottawa_relevance.csv",
                   "bigram_file" : "uottawa_bigram.csv"}
CORPUS[REUTERS] = {"source" : "/home/tjm/Documents/Winter2020/CSI4107/reuters21578",
                   "corpusxml" : "reuters_corpus.xml",
                   "inverted_index_file" : "reuters_inverted_index.csv",
                   "lpp_file" : "reuters_lpp.csv",
                   "bigraph_file" : "reuters_bigraph_index.csv",
                   "spelling_file" : "reuters_spelling.csv",
                   "relevance_file" : "reuters_relevance.csv",
                   "doc_by_topic" : "reuters_doc_by_topic.csv",
                   "bigram_file" : "reuters_bigram.csv"}


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
ROCCHIO_MIN = 0.4
TOPICS = ['all-topics', 'acq', 'alum', 'austdlr', 'barley', 'bfr', 'bop', 'can', 'carcass',
          'castor-oil', 'castorseed', 'citruspulp', 'cocoa', 'coconut',
          'coconut-oil', 'coffee', 'copper', 'copra-cake', 'corn', 'corn-oil',
          'cornglutenfeed', 'cotton', 'cotton-oil', 'cottonseed', 'cpi', 'cpu',
          'crude', 'cruzado', 'dfl', 'dkr', 'dlr', 'dmk', 'earn', 'f-cattle',
          'fishmeal', 'fuel', 'gas', 'gnp', 'gold', 'grain', 'groundnut',
          'groundnut-oil', 'heat', 'hk', 'hog', 'housing', 'income', 'instal-debt',
          'interest', 'inventories', 'ipi', 'iron-steel', 'jet', 'jobs',
          'l-cattle', 'lead', 'lei', 'lin-meal', 'lin-oil', 'linseed', 'lit',
          'livestock', 'lumber', 'meal-feed', 'money-fx', 'money-supply', 'naphtha',
          'nat-gas', 'nickel', 'nkr', 'notopic', 'nzdlr', 'oat', 'oilseed',
          'orange', 'palladium', 'palm-oil', 'palmkernel', 'peseta', 'pet-chem',
          'platinum', 'plywood', 'pork-belly', 'potato', 'propane', 'rand',
          'rape-meal', 'rape-oil', 'rapeseed', 'red-bean', 'reserves', 'retail',
          'rice', 'ringgit', 'rubber', 'rupiah', 'rye', 'saudriyal', 'sfr',
          'ship', 'silver', 'skr', 'sorghum', 'soy-meal', 'soy-oil', 'soybean',
          'stg', 'strategic-metal', 'sugar', 'sun-meal', 'sun-oil', 'sunseed',
          'tapioca', 'tea', 'tin', 'trade', 'veg-oil', 'wheat', 'wool', 'wpi',
          'yen', 'zinc']
MAX_QCM_SUGGESTIONS = 5
MAX_BOOLEAN_DOCS = 50
