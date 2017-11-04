import random
import time
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
        self.ratings = defaultdict(int)  # Users who rated this, and their rating.

    def __str__(self):
        return "{} - Ratings: {}".format(self.title, self.ratings)

class User:
    def __init__(self, id):
        self.id = id
        self.name = "User {}".format(id)
        self.ratings = defaultdict(int)  # Movies the user rated, and their rating.

    def __str__(self):
        return "{} - Ratings {}".format(self.name, self.ratings)


def generate_test_data(N=100):
    users = [User(i) for i in range(N)]  # 100 users exist.
    movies = [Movie(i) for i in range(N)]  # 100 movies exist.
    for movie_id in range(N):  # Iterate through movies.
        users_picked = {random.randrange(N) for _ in range(random.randrange(N))}
        movie_ratings = {}
        for user in users_picked:
            rating = random.randrange(1, 6)
            movie_ratings[user] = rating
            users[user].ratings[movie_id] = rating
        movies[movie_id].ratings = movie_ratings
    return users, movies


users, movies = generate_test_data()

# for movie in movies:
#     print(movie)

# 1 First algorithm.
start = time.time()
item_item_matrix = []
for movie_i in movies:
    movie_scores = []
    for movie_j in movies:
        users_that_rated_both_movies = movie_i.ratings.keys() & movie_j.ratings.keys()
        rating_i_vector = [movie_i.ratings[user] for user in movie_i.ratings if
                           user in users_that_rated_both_movies]
        rating_j_vector = [movie_j.ratings[user] for user in movie_j.ratings if
                           user in users_that_rated_both_movies]
        # print('(', movie_i.id, movie_j.id, ')', 'Users who rated both:', users_that_rated_both_movies, rating_i_vector, rating_j_vector)

        cos_score = cos_sim(rating_i_vector, rating_j_vector)
        # print(rating_j_vector, rating_j_vector, cos_score)
        movie_scores.append(cos_score)
    item_item_matrix.append(movie_scores)

end = time.time()

print("Algorithm #1", end - start)


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
