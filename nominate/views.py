from flask import render_template

from nominate import app
from nominate.models import Movie, User, Genre
from nominate.database import db_session
from flask import render_template

from nominate import app
from nominate.database import db_session
from nominate.models import Movie, User, Genre


@app.route("/")
def index():
    # conn = connect(app.config['DATABASE'])
    #
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM movies")
    #
    # users = get_all_users(conn)
    # all_movies = get_all_movies(conn)

    print(Movie.query.all())

    return render_template('index.html', user="Genres:", movies=Genre.query.all())


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

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

# if __name__ == "__main__":
#     # print("Hello World")
#     app.run(debug=True)  # To propagate changes.
