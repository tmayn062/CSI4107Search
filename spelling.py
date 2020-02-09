"""Spelling correction with weighted edit distance."""
# Adapted from Winter2020-CSI4107-TolerantRetrieval slides
import numpy

DEFAULT_COST = numpy.ones((26, 26), dtype=numpy.float64) * 2.


def edit_distance(word1, word2, cost_function=DEFAULT_COST):
    """Dynamic programming to calculate weighted edit distance."""
    len_word1 = len(word1)
    len_word2 = len(word2)
    array_dist = numpy.zeros((len_word2+1, len_word1+1), dtype='int32')
    # Initialization
    for i in range(len_word2+1):
        array_dist[i, 0] = i
    for j in range(len_word1+1):
        array_dist[0, j] = j
    # Reccurrence
    for i in range(1, len_word2+1):
        for j in range(1, len_word1+1):
            if word1[j-1] == word2[i-1]:
                add_fact = 0
            else:
                char_word1 = ord(word1[j-1]) - 97
                char_word2 = ord(word2[i-1]) - 97
                add_fact = cost_function[char_word1][char_word2]
            array_dist[i, j] = min(array_dist[i-1, j] + 1,
                                   array_dist[i, j-1] + 1,
                                   array_dist[i-1, j-1] + add_fact)
    return array_dist[len_word2, len_word1]
