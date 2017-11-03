import random

import numpy as np

random.seed(1)  # Consistent test data.


class User:
    def __init__(self, id, first_name):
        self.id = id
        self.first_name = first_name
        self.last_name = None
        self.email = None
        self.ratings = {}

    def __str__(self):
        return "User {} rated: {}".format(self.first_name, self.ratings)


movies = {i for i in range(10)}  # 10 movies that exist.
users = []  # All users that exist.

for i in range(10):
    movies_picked = [random.randrange(10) for _ in range(random.randrange(10))]
    user = User(i, "User {}".format(i))
    user.ratings = {movie: random.randrange(1, 6) for movie in movies_picked}
    users.append(user)

user_movie_matrix = []
for user in users:
    user_ratings = []
    print(user)
    for movie in movies:
        user_ratings.append(user.ratings.get(movie, '?'))
    user_movie_matrix.append(user_ratings)

print(np.matrix(user_movie_matrix))
