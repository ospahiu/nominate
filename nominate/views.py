from flask import render_template, json, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug import security
from werkzeug.security import check_password_hash

from nominate import app, login_manager
from nominate.database import db_session
from nominate.models import Movie, User


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/movies")
def movies():
    return render_template('movies.html', movies=sorted(Movie.query.all(), key=lambda movie: movie.title))


@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    return render_template('movie.html', movie=Movie.query.get(movie_id))


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    # _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    # validate the received values
    if _name and _password:
        _hashed_password = security.generate_password_hash(_password)
        print(_name, _hashed_password)
        user = User(username=_name, passcode=_hashed_password)
        db_session.add(user)
        db_session.commit()
        return json.dumps({'message': 'User created successfully !'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/search')
def search():
    # read the posted values from the UI
    _query = request.args.get('query')
    print(_query)
    print("hit")
    # validate the received values
    if _query:
        return render_template('results.html', movies=Movie.query.filter(Movie.title.ilike(_query)).all())
        # json.dumps({'message': '{}'.format(_query)})
    else:
        return render_template('error.html', error='No search text provided.')



@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    # try:
    _username = request.form['inputUsername']
    _password = request.form['inputPassword']
    user = User.query.filter(User.username == _username).first()
    if user:
        if not user.passcode or check_password_hash(user.passcode, _password):
            print(user)
            login_user(user)
            return redirect("/dashboard")
    return render_template('error.html', error='Wrong Email address or Password.')


@app.route('/dashboard')
@login_required
def userHome():
    movies = [Movie.query.get(rating.movieid) for rating in current_user.ratings]
    # print(movies[0].average_rating)
    return render_template('dashboard.html', movies=movies)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('error.html', error="You've logged out successfully.")


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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

# if __name__ == "__main__":
#     # print("Hello World")
#     app.run(debug=True)  # To propagate changes.
