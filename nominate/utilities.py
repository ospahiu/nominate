import random

import numpy as np

from nominate.models import User, Movie


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


def generate_test_data(N=100):
    """
    Generate fake randomized ratings, and assign them to both a set of users, as well as
    a set of movies.
    :param N: How many users, and movies created respectively.
    :return: Users, and Movies populated with ratings.
    """
    users = [User(id=i, username=None, passcode=None) for i in range(N)]  # 100 users exist.
    movies = [Movie(id=i, title=None, director=None, plot=None, year=None) for i in range(N)]  # 100 movies exist.
    for movie_id in range(N):  # Iterate through movies.
        users_picked = {random.randrange(N) for _ in range(random.randrange(N))}
        movie_ratings = {}
        for user in users_picked:
            rating = random.randrange(1, 6)
            movie_ratings[user] = rating
            users[user].ratings[movie_id] = rating
        movies[movie_id].ratings = movie_ratings
    return users, movies
