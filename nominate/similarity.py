from collections import defaultdict

from nominate.database import db_session
from nominate.models import Movie, Similarity
from nominate.utilities import cos_sim


# random.seed(1)  # Consistent test data.
#
# conn = sqlite3.connect('nominate')
#
#
# def get_all_movies(connection):
#     movies = {}
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM movies")
#     rows = cursor.fetchall()
#     for movie_result in rows:
#         movie = Movie(*movie_result)
#         cursor.execute("SELECT userid, rating FROM ratings WHERE movieid=?", (movie.id,))
#         ratings = cursor.fetchall()
#         for user_id, rating in ratings:
#             movie.ratings[user_id] = rating
#         movies[movie.id] = movie
#         # print(movie)
#     return movies
#
#
# def get_all_users(connection):
#     users = {}
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM users")
#     rows = cursor.fetchall()
#     for user_result in rows:
#         user = User(*user_result)
#         cursor.execute("SELECT movieid, rating FROM ratings WHERE userid=?", (user.id,))
#         ratings = cursor.fetchall()
#         for movieid, rating in ratings:
#             user.ratings[movieid] = rating
#         users[user.id] = user
#         # print(movie)
#     return users
#
#
# def get_user_by_id(connection, id):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE userid=?", (id,))
#     result = cursor.fetchone()
#     return User(*result) if result else None
#
#
# def get_movie_by_id(connection, id):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM movies WHERE movieid=?", (id,))
#     result = cursor.fetchone()
#     return Movie(*result) if result else None
#
#
# movies = get_all_movies(conn)
# users = get_all_users(conn)
#
#
# print(users[4])
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


def compute_item_based_similarity_model1():
    # item_item_matrix = defaultdict(int)
    similarity_counter = 0
    for movie_i in Movie.query.all():
        users_i = {rating.userid: rating.rating for rating in movie_i.ratings}
        for movie_j in Movie.query.all():
            users_j = {rating.userid: rating.rating for rating in movie_j.ratings}
            users_that_rated_both_movies = users_i.keys() & users_j.keys()

            if users_that_rated_both_movies:
                ratings_i = [rating.rating for rating in movie_i.ratings if
                             rating.userid in users_that_rated_both_movies]
                ratings_j = [rating.rating for rating in movie_j.ratings if
                             rating.userid in users_that_rated_both_movies]
                cos_score = cos_sim(ratings_i, ratings_j)
                query = Similarity.query \
                    .filter(Similarity.movieid_i == movie_i.movieid) \
                    .filter(Similarity.movieid_i == movie_i.movieid)
                similarity_exists = db_session.query(query.exists()).scalar()

                if not similarity_exists:
                    similarity = Similarity(movie_i=movie_i.movieid,
                                            movie_j=movie_j.movieid,
                                            cosine_similarity_score=cos_score)
                    db_session.add(similarity)
                    # db_session.commit()
                elif query.first().cosine_similarity_score != cos_score:
                    # print(similarity_exists, cos_score, query.first().cosine_similarity_score)
                    query.update(dict(cosine_similarity_score=cos_score))
                    similarity_counter += 1
                    # db_session.commit()
                else:
                    # print("No change in score")
                    similarity_counter += 1


                    # item_item_matrix[(movie_i.movieid, movie_j.movieid)] = cos_score
    print(similarity_counter)

    # for purchased_movie in purchased_movies:
    #     # print(movie, purchased_movie)
    #     total_similarities += 1
    # print(total_similarities, "movies to compare")


    # for movie_i in Movie.query.all()[:10]:
    #     for movie_j in Movie.query.all()[:10]:
    #         ratings_i = db_session.query(Rating).filter(Rating.movieid == movie_i.movieid).where.all()
    #         ratings_j = db_session.query(Rating).filter(Rating.movieid == movie_j.movieid).all()
    #
    #         print("Movie i:", movie_i.movieid, "Movie j:", movie_j.movieid, "Ratings 1:", len(ratings_i))
    #         print("Ratings 2:", len(ratings_j))


compute_item_based_similarity_model1()

def dump_item_to_item_matrix(connection, item_item_matrix):
    cursor = connection.cursor()
    for (movie_i, movie_j), cosine_similarity_score in item_item_matrix.items():
        items = movie_i, movie_j, float(cosine_similarity_score)
        cursor.execute('INSERT INTO similarities (movieid_i, movieid_j, cosine_similarity_score) VALUES (?,?,?)', items)
    connection.commit()


#
# start = time.time()
# item_item_matrix = compute_item_based_similarity_model(users=users, movies=movies)
# print(item_item_matrix)
# print(len(item_item_matrix))
#
# end = time.time()


def dump_predictive_ratings_matrix(connection, predictive_ratings):
    cursor = connection.cursor()
    for (user_id, movie_id), predictive_rating in predictive_ratings.items():
        items = user_id, movie_id, predictive_rating
        cursor.execute('INSERT INTO predictive_ratings1 (movieid, userid, predictive_rating) VALUES (?,?,?)', items)
    connection.commit()


# print("Algorithm #2", end - start)
#
# user = users[1]
# movie = movies[1]
#
# print(user, movie)

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

#
#
# print(compute_predictive_ratings(users, movies, item_item_matrix))
#
# conn.close()
#



# print("----------------Test cases ---------------")
# print("Test Case 1:", item_item_matrix[(22, 99)])
# print("Test Case 2:", item_item_matrix[(15, 87)])
# print("Test Case 3:", item_item_matrix[(99, 66)])
# print("Test Case 4:", item_item_matrix[(91, 0)])
# print("Test Case 4:", item_item_matrix[(67, 95)])
# print("Test Case 4:", item_item_matrix[(73, 23)])
# print("Test Case 4:", item_item_matrix[(51, 8)])
# print("Test Case 4:", item_item_matrix[(42, 79)])
# print("Test Case 4:", item_item_matrix[(10, 7)])
