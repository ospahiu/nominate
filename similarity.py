import random
from collections import defaultdict

import numpy as np

random.seed(1)  # Consistent test data.


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


class Movie:
    def __init__(self, id):
        self.id = id
        self.title = "Movie {}".format(id)
        self.ratings = defaultdict(int)

    def __str__(self):
        return "{} - Ratings: {}".format(self.title, self.ratings)

class User:
    def __init__(self, id, first_name):
        self.id = id
        self.first_name = first_name
        self.last_name = None
        self.email = None
        self.ratings = {}

    def __str__(self):
        return "User {}".format(self.first_name)


movies = []  # 10 movies that exist.
for i in range(10):
    users_picked = [random.randrange(10) for _ in range(random.randrange(10))]
    movie = Movie(i)
    movie.ratings = {user: random.randrange(1, 6) for user in users_picked}
    movies.append(movie)
users = []  # All users that exist.

# for movie in movies:
#     print(movie)

item_item_matrix = []
for movie_i in movies:
    movie_scores = []
    for movie_j in movies:
        users_that_rated_both_movies = movie_i.ratings.keys() & movie_j.ratings.keys()
        rating_i_vector = [movie_i.ratings[user] for user in movie_i.ratings.keys() if
                           user in users_that_rated_both_movies]
        rating_j_vector = [movie_j.ratings[user] for user in movie_j.ratings.keys() if
                           user in users_that_rated_both_movies]
        print('(', movie_i.id, movie_j.id, ')', 'Users who rated both:', users_that_rated_both_movies, rating_i_vector,
              rating_j_vector)

        cos_score = cos_sim(rating_i_vector, rating_j_vector)
        # print(rating_j_vector, rating_j_vector, cos_score)
        movie_scores.append(cos_score)
    item_item_matrix.append(movie_scores)

for movie_scores in item_item_matrix:
    print(movie_scores)
for movie in movies:
    print(movie)


# for i in range(10):
#     movies_picked = [random.randrange(10) for _ in range(random.randrange(10))]
#     user = User(i, "User {}".format(i))
#     user.ratings = {movie: random.randrange(1, 6) for movie in movies_picked}
#     users.append(user)

# user_movie_matrix = []
# for user in users:
#     user_ratings = []
#     print(user)
#     for movie in movies:
#         user_ratings.append(user.ratings.get(movie, '?'))
#     user_movie_matrix.append(user_ratings)
# print(sorted(movies))
# print(np.matrix(user_movie_matrix))
