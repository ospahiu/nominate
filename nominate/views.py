from collections import defaultdict

from flask import render_template, json, request, redirect
from flask_login import login_required, login_user, logout_user, current_user, confirm_login
from werkzeug import security
from werkzeug.security import check_password_hash

from nominate import app, login_manager
from nominate.database import db_session
from nominate.models import Movie, User, Rating


@app.route("/")
def index():
    compute_item_based_similarity_model()
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/movies")
def movies():
    return render_template('movies.html', movies=sorted(Movie.query.all(), key=lambda movie: movie.title))


@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    user_rating = None
    if current_user.is_authenticated:
        user_rating = Rating.query \
            .filter(Rating.userid == current_user.userid) \
            .filter(Rating.movieid == movie_id).first()
    return render_template('movie.html', movie=Movie.query.get(movie_id), user_rating=user_rating)


@app.route('/showSignUp')
def showSignUp():
    if current_user.is_authenticated:
        return redirect("/")
    return render_template('signup.html')


@login_required
@app.route('/rate/<int:movie_id>', methods=['POST'])
def rate(movie_id):
    rating_value = int(request.form["star"])
    query = Rating.query. \
        filter(Rating.userid == current_user.userid) \
        .filter(Rating.movieid == movie_id)
    has_user_rated_movie = db_session.query(query.exists()).scalar()

    if not has_user_rated_movie:
        # print("Not_rated")
        rating = Rating(userid=current_user.userid, movieid=movie_id, rating=rating_value)
        db_session.add(rating)
        db_session.commit()
    elif query.first().rating != rating_value:
        query.update(dict(rating=rating_value))
        # print("Rated differently.", rating)
        db_session.commit()
    # print(current_user.username, "Rating:", rating_value, Movie.query.get(movie_id).title)
    # print("Rate hit")
    return json.dumps({'message': '/rate hit.'})


def compute_item_based_similarity_model():
    item_item_matrix = defaultdict(int)
    current_movie_ratings_to_per_shared_users = defaultdict(list)
    ratings_to_compare_to_per_shared_users = defaultdict(list)

    for movie_i in Movie.query.all()[:10]:
        for movie_j in Movie.query.all()[:10]:
            ratings_i = db_session.query(Rating).filter(Rating.movieid == movie_i.movieid).all()
            ratings_j = db_session.query(Rating).filter(Rating.movieid == movie_j.movieid).all()

            print("Movie i:", movie_i.movieid, "Movie j:", movie_j.movieid, "Ratings 1:", len(ratings_i))
            print("Ratings 2:", len(ratings_j))


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
            confirm_login()
            return redirect("/dashboard")
    return render_template('error.html', error='Wrong Email address or Password.')


@app.route('/dashboard')
@login_required
def userHome():
    # movies = [Movie.query.get(rating.movieid) for rating in current_user.ratings]
    # print(movies[0].average_rating)
    return render_template('dashboard.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('error.html', error="You've logged out successfully.")


@app.route('/showSignIn')
def showSignin():
    if current_user.is_authenticated:
        return redirect("/")
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

# compute_item_based_similarity_model()
#     # print("Hello World")
#     app.run(debug=True)  # To propagate changes.
