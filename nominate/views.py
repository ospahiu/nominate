from flask import render_template, json, request, redirect
from flask_login import login_required, login_user, logout_user, current_user, confirm_login
from werkzeug import security
from werkzeug.security import check_password_hash

from nominate import app, login_manager
from nominate.database import db_session
from nominate.models import Movie, User, Rating
from nominate.similarity import compute_item_based_similarity_model, compute_predictive_ratings


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
@app.route('/generateRecommendations', methods=['POST'])
def similarity():
    if current_user.is_authenticated:
        if current_user.username != 'admin':
            return redirect("/")
        compute_item_based_similarity_model.delay()
        compute_predictive_ratings.delay()
        return str(200)
    return str(403)


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error.html', error='Page forbidden.'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found.'), 404

@login_required
@app.route('/rate/<int:movie_id>', methods=['POST'])
def rate(movie_id):
    rating_value = int(request.form["star"])
    query = Rating.query. \
        filter(Rating.userid == current_user.userid) \
        .filter(Rating.movieid == movie_id)
    has_user_rated_movie = db_session.query(query.exists()).scalar()

    if not has_user_rated_movie:
        rating = Rating(userid=current_user.userid, movieid=movie_id, rating=rating_value)
        db_session.add(rating)
        db_session.commit()
    elif query.first().rating != rating_value:
        query.update(dict(rating=rating_value))
        db_session.commit()
    return json.dumps({'message': '/rate hit.'})


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    # _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    # validate the received values
    if _name and _password:
        _hashed_password = security.generate_password_hash(_password)
        user = User(username=_name, passcode=_hashed_password)
        db_session.add(user)
        db_session.commit()
        login_user(user)
        confirm_login()
        return redirect("/dashboard")
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/search')
def search():
    # read the posted values from the UI
    _query = request.args.get('query')
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
            login_user(user)
            confirm_login()
            return redirect("/dashboard")
    return render_template('error.html', error='Wrong Email address or Password.')


@app.route('/dashboard')
@login_required
def userHome():
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

