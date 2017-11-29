import numpy as np


def cos_sim(vector_i, vector_j):
    """
    Simple cosine similarity formula implemented using length normalization.
    Numpy is used to perform norm, and dot product operations on the vectors.
    :param document_i: document vector
    :param query_vector: query vector
    :return: cosine of the angle between the query and document vector
    """
    A = np.array(vector_i)
    B = np.array(vector_j)
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))
