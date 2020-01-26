"""Build a dictionary of terms and index them."""


def build_it(corpus_filename: str,
             remove_stopwords=True, do_stemming=True, do_normalize=True):
    """Build a dictionary from the pre-processed corpus."""
    return ['test', 'computer', 'optimize']


def create_index(dictionary: str):
    """Associate dictionary terms to documents."""
    """Create a file with a set of doc ids and weight for each term"""
