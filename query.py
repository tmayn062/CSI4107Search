"""Process the query in the same way the text is processed."""
import preprocess_text


def process(query_str: str,
            remove_stopwords=True, do_stemming=True, do_normalize=True):
    """Process a query based on the processing parameters."""
    processed_query = preprocess_text.tokenize(query_str)
    if remove_stopwords:
        processed_query = preprocess_text.remove_stopwords(processed_query)
    if do_stemming:
        processed_query = preprocess_text.stem_text(processed_query)
    if do_normalize:
        processed_query = preprocess_text.normalize(processed_query)
    return processed_query
