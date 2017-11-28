import statistics

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from nominate.database import Base


class Movie(Base):
    __tablename__ = 'movies'
    movieid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(), nullable=False)
    director = Column(String())
    plot = Column(String())
    year = Column(Integer)
    genres = relationship('MovieGenre', backref='movie')
    ratings = relationship('Rating', backref='movie')
    similarities = relationship('Similarity', backref='movie')

    @hybrid_property
    def reviewers(self):
        return [User.query.get(rating.userid) for rating in self.ratings]

    @hybrid_property
    def similar_movies(self):
        return [Movie.query.get(similarity.movieid_j)
                for similarity in
                sorted(self.similarities, key=lambda similarity: similarity.cosine_similarity_score, reverse=True)
                if similarity.movieid_j != self.movieid]

    @hybrid_property
    def average_rating(self):
        if len(self.ratings):
            return round(statistics.mean(rating.rating for rating in self.ratings), 1)
        return None


    def __repr__(self):
        return "<Id: {}, Title: {}, Genres {}, Ratings: {}, Similariites: {}".format(self.movieid,
                                                                                     self.title,
                                                                                     self.genres,
                                                                                     self.ratings,
                                                                                     self.similarities)


class Similarity(Base):
    __tablename__ = 'similarities'
    similarityid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movieid_i = Column(Integer, ForeignKey('movies.movieid'), nullable=False)
    movieid_j = Column(Integer, nullable=False)
    cosine_similarity_score = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint('movieid_i', 'movieid_j'), UniqueConstraint('movieid_j', 'movieid_i'))

    def __repr__(self):
        return "<Id: {}, MovieId_i: {}, MovieId_j: {}, Cos score: {}>".format(self.similarityid,
                                                                              self.movieid_i,
                                                                              self.movieid_j,
                                                                              self.cosine_similarity_score)


class Rating(Base):
    __tablename__ = 'ratings'
    ratingid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    userid = Column(Integer, ForeignKey('users.userid'), nullable=False)
    movieid = Column(Integer, ForeignKey('movies.movieid'), nullable=False)
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Id: {}, userid: {}, movieid: {}, rating: {}>".format(self.ratingid,
                                                                      self.userid,
                                                                      self.movieid,
                                                                      self.rating)


class PredictiveRating(Base):
    __tablename__ = 'predictive_ratings'
    predictive_ratingid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    userid = Column(Integer, ForeignKey('users.userid'), nullable=False)
    movieid = Column(Integer, ForeignKey('movies.movieid'), nullable=False)
    predictive_rating = Column(Float, nullable=False)

    def __repr__(self):
        return "<Id: {}, userid: {}, movieid: {}, rating: {}>".format(self.predictive_ratingid,
                                                                      self.userid,
                                                                      self.movieid,
                                                                      self.predictive_rating)


class User(UserMixin, Base):
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(), nullable=False, unique=True)
    passcode = Column(String())
    ratings = relationship('Rating', backref='user')
    predictive_ratings = relationship('PredictiveRating', backref='user')

    @hybrid_property
    def rated_movies(self):
        return {Movie.query.get(rating.movieid): rating.rating for rating in self.ratings}

    @hybrid_property
    def predictive_movies(self):
        return [Movie.query.get(predictive_rating.movieid)
                for predictive_rating in
                sorted(self.predictive_ratings,
                       key=lambda predictive_rating: predictive_rating.predictive_rating,
                       reverse=True)]

    def get_id(self):
        return self.userid


    def __repr__(self):
        return "<Id: {}, Name: {}, Ratings: {}>".format(self.userid, self.username, self.ratings)


class Genre(Base):
    __tablename__ = 'genres'
    genreid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    genre = Column(String(), nullable=False, unique=True)

    def __repr__(self):
        return '<Id: {}, Genre: {}>'.format(self.genreid, self.genre)


class MovieGenre(Base):
    __tablename__ = 'movie_genres'
    movie_genreid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    movieid = Column(Integer, ForeignKey('movies.movieid'), nullable=False)
    genreid = Column(Integer, ForeignKey('genres.genreid'), nullable=False)
    genre = relationship('Genre', backref='movie_genres')

    def __repr__(self):
        return '<Movie Id: {}, Genre Id: {}, Genre: {}>'.format(self.movieid, self.genreid, self.genre)
