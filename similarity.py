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
    def __init__(self, id, title, director, plot, year):
        self.id = id
        self.title = title
        self.director = director
        self.plot = plot
        self.year = year
        self.ratings = defaultdict(int)  # Users who rated this, and their rating.

    def __str__(self):
        return "{} - Ratings: {}".format(self.title, self.ratings)

class User:
    def __init__(self, id, username, passcode):
        self.id = id
        self.username = username
        self.passcode = passcode
        self.ratings = defaultdict(int)  # Movies the user rated, and their rating.

    def __str__(self):
        return "{} - Ratings {}".format(self.username, self.ratings)


# def generate_test_data(N=100):
#     users = [User(i) for i in range(N)]  # 100 users exist.
#     movies = [Movie(i) for i in range(N)]  # 100 movies exist.
#     for movie_id in range(N):  # Iterate through movies.
#         users_picked = {random.randrange(N) for _ in range(random.randrange(N))}
#         movie_ratings = {}
#         for user in users_picked:
#             rating = random.randrange(1, 6)
#             movie_ratings[user] = rating
#             users[user].ratings[movie_id] = rating
#         movies[movie_id].ratings = movie_ratings
#     return users, movies
#
#

conn = sqlite3.connect('nominate.db')


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
        cursor.execute('INSERT INTO predictive_ratings (movieid, userid, predictive_rating) VALUES (?,?,?)', items)
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
dump_predictive_ratings_matrix(conn, compute_predictive_ratings(users, movies, item_item_matrix))
conn.close()




# for username in usernames:

        # items = (1,)
# c.execute('INSERT INTO users (username) VALUES (?)', (username,))

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

# genres = {"Action": 1,
#           "Adventure": 2,
#           "Animation": 3,
#           "Children": 4,
#           "Comedy": 5,
#           "Crime": 6,
#           "Documentary": 7,
#           "Drama": 8,
#           "Fantasy": 9,
#           "Film-Noir": 10,
#           "Horror": 11,
#           "IMAX": 12,
#           "Musical": 13,
#           "Mystery": 14,
#           "Romance": 15,
#           "Sci-Fi": 16,
#           "Thriller": 17,
#           "War": 18,
#           "Western": 19}
#
#
# usernames = ["AlertQuant",
# "Annadayer",
# "ArticlesPhat",
# "Atmellibi",
# "Beamburd",
# "BeastEpicReport",
# "Blervite",
# "BlueGame",
# "Bottlemed",
# "BuddieFluent",
# "Bufficoner",
# "Camella",
# "CanyonsReport",
# "Capolassed",
# "Carteriher",
# "Celkage",
# "Cleverrylh",
# "CoverCist",
# "Curabouc",
# "DanceCountry",
# "Deriells",
# "Diagonaleu",
# "Diumphon",
# "Drakergile",
# "Dramours",
# "Draventroo",
# "Etchicide",
# "Faegoric",
# "FinestFashion",
# "Firstilli",
# "Foprisom",
# "Freextech",
# "Fusional",
# "Gameriusaro",
# "Gausefra",
# "GetVander",
# "Griffonli",
# "HaroLovely",
# "Heidexpe",
# "HolyCleverDailies",
# "HomeyGrand",
# "HumanSlim",
# "Hydrain",
# "InloveWil",
# "IzPenguin",
# "JameYounger",
# "Keeperzesi",
# "Kennaut",
# "Kurocktati",
# "Landerra",
# "Lapilorth",
# "Lastinghall",
# "LatestTara",
# "Limerivell",
# "Matibign",
# "MessageStronger",
# "MonkeyAlly",
# "MoTinnysMountain",
# "MountainBig",
# "MrPlace",
# "Nanores",
# "NearlyRunning",
# "NephewBWith",
# "Nepheworal",
# "Novamrofo",
# "PatAni",
# "PersonDaily",
# "Phatorksta",
# "Phiaenette",
# "PinCrawler",
# "Pingotepl",
# "ProAce",
# "ReallyPassion",
# "Reincock",
# "Reporterao",
# "RobCinco",
# "Roltast",
# "RomanticMessages",
# "Saltendo",
# "SarenPuppyNephew",
# "Seekellaher",
# "ShatQuoteCart",
# "ShayFlashTeenage",
# "Shutotrol",
# "Singhillet",
# "Soillpbx",
# "Sparketpipe",
# "Specialsie",
# "SpecialsRocker",
# "Starticle",
# "Steadem",
# "StroonsBoyUpdate",
# "Subgenven",
# "Synoline",
# "Tearmation",
# "TheborgSolomon",
# "ThugGuy",
# "TimesThega",
# "Toyoneymacy",
# "UpdateAlly"]
