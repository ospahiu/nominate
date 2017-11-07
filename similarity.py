import random
import sqlite3
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
# start = time.time()
# item_item_matrix = []
# for movie_i in movies:
#     movie_scores = []
#     for movie_j in movies:
#         users_that_rated_both_movies = movie_i.ratings.keys() & movie_j.ratings.keys()
#         cos_score = 'nan'
#         if users_that_rated_both_movies:
#             rating_i_vector = [movie_i.ratings[user] for user in movie_i.ratings if
#                                user in users_that_rated_both_movies]
#             rating_j_vector = [movie_j.ratings[user] for user in movie_j.ratings if
#                                user in users_that_rated_both_movies]
#             cos_score = cos_sim(rating_i_vector, rating_j_vector)
#         movie_scores.append(cos_score)
#     item_item_matrix.append(movie_scores)
#
# end = time.time()
#
# print("Algorithm #1", end - start)

# -----------------------------------------------------------------------------

# 2 Second algorithm.

def compute_item_based_similarity_model(users, movies):
    item_item_matrix = defaultdict(int)

    for movie in movies:
        current_movie_ratings_to_per_shared_users = defaultdict(list)
        ratings_to_compare_to_per_shared_users = defaultdict(list)

        for user_id, rating in movie.ratings.items():  # Customers that bought Product 1
            for movie_id_bought_by_user, rating_j in users[user_id].ratings.items():
                if user_id in movies[movie_id_bought_by_user].ratings:
                    current_movie_ratings_to_per_shared_users[movie_id_bought_by_user].append(rating)
                    ratings_to_compare_to_per_shared_users[movie_id_bought_by_user].append(rating_j)

        for movie_id, ratings in ratings_to_compare_to_per_shared_users.items():
            similarity_score = cos_sim(current_movie_ratings_to_per_shared_users[movie_id], ratings)
            item_item_matrix[(movie.id, movie_id)] = similarity_score
    return item_item_matrix

start = time.time()
item_item_matrix = compute_item_based_similarity_model(users=users, movies=movies)
print(len(item_item_matrix))
end = time.time()

print("Algorithm #2", end - start)

user = users[0]
movie = movies[3]


# print(user, movie)

def predict_rating(user, movie):
    weighted_sum = 0
    similarity_sum = 0
    for movie_id, rating in user.ratings.items():
        similarity = item_item_matrix[(movie_id, movie.id)]
        weighted_sum += rating * similarity
        similarity_sum += similarity
    return weighted_sum / similarity_sum  # Returns prediction for given user and movie.


print(predict_rating(user, movie))

conn = sqlite3.connect('nominate.db')
c = conn.cursor()
genres = {"Action": 1,
          "Adventure": 2,
          "Animation": 3,
          "Children": 4,
          "Comedy": 5,
          "Crime": 6,
          "Documentary": 7,
          "Drama": 8,
          "Fantasy": 9,
          "Film-Noir": 10,
          "Horror": 11,
          "IMAX": 12,
          "Musical": 13,
          "Mystery": 14,
          "Romance": 15,
          "Sci-Fi": 16,
          "Thriller": 17,
          "War": 18,
          "Western": 19}

for user in users:
    for movie_id, rating in user.ratings.items():
        items = user.id + 1, movie_id + 1, rating
        # items = (1,)
        # c.execute('INSERT INTO ratings (userid, movieid, rating) VALUES (?,?,?)', items)

#
# with open("/Users/ospahiu/Downloads/ml-20m 2/movies.csv", 'r') as movies:
#     count = 0
#     next(movies)
#     for line in movies:
#         parsed_movie_line = line.split(',')
#         # print(parsed_movie_line)
#         id = parsed_movie_line[0],
#         title = parsed_movie_line[1].strip()
#         movie_genres = parsed_movie_line[-1].split('|')
#         # print(parsed_movie_line)
#         # print(movie_genres)
#         for movie_genre in movie_genres:
#             print(id, genres[movie_genre.strip()])
#             # c.execute('INSERT INTO movie_genres (movieid, genreid) VALUES (?,?)', (int(id[0]), genres[movie_genre.strip()]))
#         count += 1
#         if count == 99:
#             break

conn.commit()
conn.close()


# print(item_item_matrix)
# len_items = len([ item for l in item_item_matrix for item in l if item != 'nan'])
# print(item_item_matrix_2)
# print(len(item_item_matrix_2), len_items)


# print("----------------Test cases ---------------")
# print("Test Case 1:", item_item_matrix[22][99], item_item_matrix_2[(22, 99)])
# print("Test Case 2:", item_item_matrix[15][87], item_item_matrix_2[(15, 87)])
# print("Test Case 3:", item_item_matrix[99][66], item_item_matrix_2[(99, 66)] if item_item_matrix_2[(99, 66)] != 0 else 'nan')
# print("Test Case 4:", item_item_matrix[91][0] , item_item_matrix_2[(91, 0)])
# print("Test Case 4:", item_item_matrix[67][95] , item_item_matrix_2[(67, 95)])
# print("Test Case 4:", item_item_matrix[73][23] , item_item_matrix_2[(73, 23)])
# print("Test Case 4:", item_item_matrix[51][8] , item_item_matrix_2[(51, 8)])
# print("Test Case 4:", item_item_matrix[42][79] , item_item_matrix_2[(42, 79)])
# print("Test Case 4:", item_item_matrix[10][7] , item_item_matrix_2[(10, 7)])
