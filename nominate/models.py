from collections import defaultdict

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

    def __init__(self, id, title, director, plot, year, genres=None):
        self.id = id
        self.title = title
        self.director = director
        self.plot = plot
        self.year = year
        self.genres = genres
        self.ratings = defaultdict(int)  # Users who rated this, and their rating.

    def __str__(self):
        return "<Id: {}, Title: {}, Genres {}".format(self.movieid, self.title, self.genres)


class User:
    def __init__(self, id, username, passcode):
        self.id = id
        self.username = username
        self.passcode = passcode
        self.ratings = defaultdict(int)  # Movies the user rated, and their rating.

    def __str__(self):
        return "{} - Ratings {}".format(self.username, self.ratings)


class Genre(Base):
    __tablename__ = 'genres'
    genreid = Column(Integer, primary_key=True)
    genre = Column(String())

    def __init__(self, genre=None):
        self.genre = genre

    def __str__(self):
        return '<Id: {}, Genre: {}>'.format(self.genreid, self.genre)


class MovieGenre(Base):
    __tablename__ = 'movie_genres'
    movie_genresid = Column(Integer, primary_key=True)
    movieid = Column(Integer, ForeignKey('movies.movieid'))
    genreid = Column(Integer, ForeignKey('genres.genreid'))
    genre = relationship('Genre', backref='movie_genres')

    def __init__(self, genre=None):
        self.genre = genre

    def __repr__(self):
        return '<Movie Id: {}, Genre Id: {}, Genre: {}>'.format(self.movieid, self.genreid, self.genre)
