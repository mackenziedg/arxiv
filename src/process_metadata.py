from collections import Counter
import math

import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import numpy as np
import pandas as pd


def dot(a, b):
    """Takes two sparse vectors and finds their dot products.
    
    Parameters
    ----------
    a, b -- Sparse vectors represented as Python Counters
    
    Returns
    -------
    c -- Dot product of `a` and `b`
    """
    c = 0
    for k in a.keys() & b.keys():
        c += a[k] * b[k]
    return c


def norm(a):
    """Finds the L2 norm of a sparse vector.
    
    Parameters
    ----------
    a -- Sparse vector represented as a Python Counter
    
    Returns
    -------
    b -- Norm of `a`
    """
    return np.linalg.norm(np.fromiter(a.values(), dtype=int), 2)


def cosine_similarity(doc1, doc2):
    """Finds the cosine similarity between two documents.
    
    Parameters
    ----------
    doc1, doc2 -- Sparse vectors of word counts represented as Python Counters
    
    Returns
    -------
    Cosine similarity between `doc1` and `doc2`
    """
    return dot(doc1, doc2)/(norm(doc1)*norm(doc2))


def cosine_distance(doc1, doc2):
    """Finds the cosine distance between two documents.
    
    Parameters
    ----------
    doc1, doc2 -- Sparse vectors of word counts represented as Python Counters
    
    Returns
    -------
    Cosine distance between `doc1` and `doc2`
    """
    return 1-cosine_similarity(doc1, doc2)


def most_similar(doc, n=100):
    """Returns the n most similar documents.
    
    Parameters
    ----------
    doc -- Document of interest
    n -- Number of results to return (optional)
    
    Returns
    -------
    similarities -- A size-n vector of document similarities, ignoring the same document"""
    similarities = ca_counts.apply(lambda x: cosine_similarity(doc, x))
    return similarities.sort_values(ascending=False)[1:(1+n)]


if __name__ == "__main__":
    stopwords = set(stopwords.words('english'))
    
    #Read in the data
    df = pd.read_csv("../data/full_arxiv_cs_clean.csv", index_col="Unnamed: 0", low_memory=False)
    selected = df[~df.abstract.isnull()][['abstract', 'id']]
    
    #Process and clean the abstracts
    clean_abstracts = selected.abstract.str.lower()
    clean_abstracts = clean_abstracts.str.replace(r"[.()$,:;\"%{}\-\\/<>+=_~'^]", " ")
    clean_abstracts = clean_abstracts.str.replace(r" {2,}", " ")
    clean_abstracts = clean_abstracts.apply(lambda x: [i for i in x.strip().split() if i not in stopwords])
    
    #Generate word counts
    ca_counts = clean_abstracts.apply(lambda x: Counter(x))
    pd.DataFrame({"counts": ca_counts}).to_csv("../data/full_arxiv_cs_counts.csv", encoding="utf8")
    
