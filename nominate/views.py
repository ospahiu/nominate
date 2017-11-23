from flask import render_template, json, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug import security
from werkzeug.security import check_password_hash

from nominate import app, login_manager
from nominate.database import db_session
from nominate.models import Movie, User


@app.route("/")
def index():
    # conn = connect(app.config['DATABASE'])
    #
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM movies")
    #
    # users = get_all_users(conn)
    # all_movies = get_all_movies(conn)
    movies = []
    for movie in Movie.query.all():
        movie_dict = movie.__dict__
        movie_dict.pop('_sa_instance_state', None)
        movies.append(movie_dict)
    return render_template('index.html', movies=[movies[-1]])

@app.route("/movies")
def movies():
    return render_template('movies.html', movies=Movie.query.all())


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
    return redirect('/')


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
