import random
import sqlite3
import time
from collections import defaultdict

from nominate.models import Movie, User
from nominate.utilities import cos_sim

random.seed(1)  # Consistent test data.

conn = sqlite3.connect('nominate')


def get_all_movies(connection):
    movies = {}
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    for movie_result in rows:
        movie = Movie(*movie_result)
        cursor.execute("SELECT userid, rating FROM ratings WHERE movieid=?", (movie.id,))
        ratings = cursor.fetchall()
        for user_id, rating in ratings:
            movie.ratings[user_id] = rating
        movies[movie.id] = movie
        # print(movie)
    return movies


def get_all_users(connection):
    users = {}
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for user_result in rows:
        user = User(*user_result)
        cursor.execute("SELECT movieid, rating FROM ratings WHERE userid=?", (user.id,))
        ratings = cursor.fetchall()
        for movieid, rating in ratings:
            user.ratings[movieid] = rating
        users[user.id] = user
        # print(movie)
    return users


def get_user_by_id(connection, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE userid=?", (id,))
    result = cursor.fetchone()
    return User(*result) if result else None


def get_movie_by_id(connection, id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE movieid=?", (id,))
    result = cursor.fetchone()
    return Movie(*result) if result else None


movies = get_all_movies(conn)
users = get_all_users(conn)


print(users[4])
# 2 Second algorithm.

def compute_item_based_similarity_model(users, movies):
    item_item_matrix = defaultdict(int)

    for movie_id, movie in movies.items():
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
print(item_item_matrix)
print(len(item_item_matrix))
end = time.time()


def dump_item_to_item_matrix(connection, item_item_matrix):
    cursor = connection.cursor()
    for (movie_i, movie_j), cosine_similarity_score in item_item_matrix.items():
        items = movie_i, movie_j, float(cosine_similarity_score)
        cursor.execute('INSERT INTO similarities (movieid_i, movieid_j, cosine_similarity_score) VALUES (?,?,?)', items)
    connection.commit()


def dump_predictive_ratings_matrix(connection, predictive_ratings):
    cursor = connection.cursor()
    for (user_id, movie_id), predictive_rating in predictive_ratings.items():
        items = user_id, movie_id, predictive_rating
        cursor.execute('INSERT INTO predictive_ratings1 (movieid, userid, predictive_rating) VALUES (?,?,?)', items)
    connection.commit()




print("Algorithm #2", end - start)

user = users[1]
movie = movies[1]

print(user, movie)

def predict_rating(user, movie, item_item_matrix):
    weighted_sum = 0
    similarity_sum = 0
    for movie_id, rating in user.ratings.items():
        similarity = item_item_matrix[(movie_id, movie.id)]
        weighted_sum += rating * similarity
        similarity_sum += similarity
    return weighted_sum / similarity_sum  # Returns prediction for given user and movie.


def compute_predictive_ratings(users, movies, item_item_matrix):
    user_prediction_model = defaultdict(int)
    for user_id, user in users.items():
        for movie_id, movie in movies.items():
            if movie_id not in user.ratings:
                predictive_rating = predict_rating(user, movie, item_item_matrix)
                user_prediction_model[(user_id, movie_id)] = predictive_rating
    return user_prediction_model


print(compute_predictive_ratings(users, movies, item_item_matrix))

conn.close()




# print("----------------Test cases ---------------")
print("Test Case 1:", item_item_matrix[(22, 99)])
print("Test Case 2:", item_item_matrix[(15, 87)])
print("Test Case 3:", item_item_matrix[(99, 66)])
print("Test Case 4:", item_item_matrix[(91, 0)])
print("Test Case 4:", item_item_matrix[(67, 95)])
print("Test Case 4:", item_item_matrix[(73, 23)])
print("Test Case 4:", item_item_matrix[(51, 8)])
print("Test Case 4:", item_item_matrix[(42, 79)])
print("Test Case 4:", item_item_matrix[(10, 7)])
