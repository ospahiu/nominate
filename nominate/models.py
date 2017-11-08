from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from nominate.database import Base


class Movie(Base):
    __tablename__ = 'movies'
    movieid = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    director = Column(String())
    plot = Column(String())
    year = Column(Integer)
    genres = relationship('MovieGenre', backref='movie')
    ratings = relationship('Rating', backref='movie')

    # def __init__(self, id, title, director, plot, year, genres=None):
    #     self.id = id
    #     self.title = title
    #     self.director = director
    #     self.plot = plot
    #     self.year = year
    #     self.genres = genres
    #     self.ratings = defaultdict(int)  # Users who rated this, and their rating.

    def __repr__(self):
        return "<Id: {}, Title: {}, Genres {} \n{}".format(self.movieid, self.title, self.genres, self.ratings)


class Rating(Base):
    __tablename__ = 'ratings'
    ratingid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    movieid = Column(Integer, ForeignKey('movies.movieid'))
    rating = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Id: {}, userid: {}, movieid: {}, rating: {}>".format(self.ratingid,
                                                                      self.userid,
                                                                      self.movieid,
                                                                      self.rating)


class User(Base):
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True)
    username = Column(String(), nullable=False)
    passcode = Column(String())
    ratings = relationship('Rating', backref='user')

    # def __init__(self, id, username, passcode):
    #     self.id = id
    #     self.username = username
    #     self.passcode = passcode
    #     self.ratings = defaultdict(int)  # Movies the user rated, and their rating.

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
