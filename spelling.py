"""Spelling correction with weighted edit distance."""
# Adapted from Winter2020-CSI4107-TolerantRetrieval slides
import numpy

default_cost = numpy.ones((26, 26), dtype=numpy.float64) * 2.


def edit_distance(word1, word2, cost_function=default_cost):
    """Dynamic programming to calculate weighted edit distance."""
    n = len(word1)
    m = len(word2)
    d = numpy.zeros((m+1, n+1), dtype='int32')
    # Initialization
    for i in range(m+1):
        d[i, 0] = i
    for j in range(n+1):
        d[0, j] = j
    # Reccurrence
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[j-1] == word2[i-1]:
                add_fact = 0
            else:
                a = ord(word1[j-1]) - 97
                b = ord(word2[i-1]) - 97
                add_fact = cost_function[a][b]
            d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + add_fact)
    return d[m, n]
