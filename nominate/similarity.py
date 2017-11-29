from nominate import celery
from nominate.database import db_session
from nominate.models import Similarity, Movie, User, PredictiveRating
from nominate.utilities import cos_sim


@celery.task
def compute_item_based_similarity_model():
    for movie_i in Movie.query.all():
        for movie_j in Movie.query.all():
            users_that_rated_both_movies = movie_i.reviewers & movie_j.reviewers
            if users_that_rated_both_movies:
                ratings_i = [rating.rating for rating in movie_i.ratings if
                             User.query.get(rating.userid) in users_that_rated_both_movies]
                ratings_j = [rating.rating for rating in movie_j.ratings if
                             User.query.get(rating.userid) in users_that_rated_both_movies]
                cos_score = cos_sim(ratings_i, ratings_j)
                query = Similarity.query \
                    .filter(Similarity.movieid_i == movie_i.movieid) \
                    .filter(Similarity.movieid_j == movie_j.movieid)
                similarity_exists = db_session.query(query.exists()).scalar()

                if not similarity_exists:
                    similarity = Similarity(movie_i=movie_i.movieid,
                                            movie_j=movie_j.movieid,
                                            cosine_similarity_score=cos_score)
                    db_session.add(similarity)
                    db_session.commit()
                elif query.first().cosine_similarity_score != cos_score:
                    query.update(dict(cosine_similarity_score=cos_score))
                    db_session.commit()


def predict_rating(user, movie):
    weighted_sum = 0
    similarity_sum = 0
    for rating in user.ratings:
        similarity = Similarity.query \
            .filter(Similarity.movieid_i == movie.movieid) \
            .filter(Similarity.movieid_j == rating.movieid) \
            .first()
        if similarity:
            weighted_sum += rating.rating * similarity.cosine_similarity_score
            similarity_sum += similarity.cosine_similarity_score
    return weighted_sum / (similarity_sum if similarity_sum else 1)  # Returns prediction for given user and movie.


@celery.task
def compute_predictive_ratings():
    for user in User.query.all():
        for movie in user.not_rated_movies:
            predictive_rating_score = predict_rating(user, movie)
            query = PredictiveRating.query \
                .filter(PredictiveRating.userid == user.userid) \
                .filter(PredictiveRating.movieid == movie.movieid)

            predictive_rating_exists = query.scalar()
            if not predictive_rating_exists:
                predictive_rating = PredictiveRating(movieid=movie.movieid,
                                                     userid=user.userid,
                                                     predictive_rating=predictive_rating_score)
                db_session.add(predictive_rating)
                db_session.commit()
            elif query.first().predictive_rating != predictive_rating_score:
                query.update(dict(predictive_rating=predictive_rating_score))
                db_session.commit()
