from collections import defaultdict


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
