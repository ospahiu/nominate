*** Assignment 3 README - PLEASE READ ***
@Author(s) Olsi Spahiu, Frank Vumbaca
@email(s)  olsi.spahiu@ryerson.ca, fvumbaca@ryerson.ca
@StdID     500569564, 500564107
@date      November 28th, 2017
@brief     Assignment 3 README.

# Nominate
Movie recommendation web application that allows users to view movies, rate them, and get personalized predictions
based on their rating behaviour, as well as the ratings of other users! The system becomes more accurate overtime as
the increase of ratings helps steer recommendations and predictions on what users might like the most.

## Introduction

The goal of this assignment is to implement a movie recommender system. Users should be able to access a website
and be able to rate movies as they deem fit. The rating system used in the application is in the form of 5 stars. Where
users can choose what ratings they would like to give on this scale. All of this information is kept in the database of
this app in 'nominate.db'. After enough ratings come through, it is advisable that you run the recommender system to
populate predictions and similar movies. This particular application takes advantage of the model-based collaborative 
filtering approach via item-to-item similarity scores.

As part of the assignment outline, we have completed every requirement including:

1) Creating a web application and front end users can access.
2) Populate the database with films, and their respective attributes.
3) Cosine-Similarity implemented similarity score.
4) Ability to generate an item-to-item matrix and store it inside of the database.
5) Ability to generate predictions for each user on movies they haven not rated and store results in the database.
6) Ability to rate movies on a per-movie basis using a 5-star system.
7) Fully fledged views to login, signup, search for movies, look at movie titles, and run recommendations.
5) Report outlining the implementation, with sample screenshots included in this zip.

## Implementation Details

This program is built around a Flask web application called Nominate. Users can sign in to their existing accounts, and
be able to view their dashboard where they can see which movies they've rated. From their users will be able to view
custom predictions on a per-user basis. The user can search for movies, and is able to click and browse though a 
catalogue of various titles. The views are all built with Jinja's web templating system, this allowing dynamic and
custom views per user. 

The core of the application rests on the database design which links users and movies and vice-versa via a Rating table. 
This table contains all user information (Please see the database diagram included in the screenshots folder of this 
zip). Similarity computation, and predictive ratings can then be executed from the data contained inside of the user's
ratings, and movie's ratings. This system is abstracted away with a Database session manager provided by Flask, as well 
as utilizing SQL-Alchemy to wrap each of my models for easy declarative database interactions.

In terms of the actual recommendation calculations; I've chosen to use a model-based collaborative filtering algorithm
since this allows me to cache my results, and store this state permanently inside of the database. The algorithm 
iterates every single movie, and then iterates over every single movie again to form a nested for-loop. From here, 
ratings where users have given TO BOTH movies are aggregated and formed as vectors of user ratings per movie, i.e.:
 
movie_ratings_i = [(User 1, 1), (User 2, 4), (User 3, 3), (User 4, 5), (User 5, 2), (User 6, 3)]
movie_ratings_j = [(User 1, 4), (User 2, 3), (User 3, 3), (User 4, 1), (User 5, 5), (User 6, 5)]
 
From here the score is calculated using the cosine similarity formula  (standard item-to-item implementation). The 
similarity matrix is then stored as rows of the following data shape:

(Movie_i, Movie_j, Cosine Similarity Score)

To the Similarity table as shown in the screenshots. The predictions are then made by accessing our newly created matrix
and finding the movies which users have not rated, and from there predicting the rating they might give them based on 
other movies they've rated. These ratings are then multiplied by the similarity score where they are essentially given
a factor based on similarity score. The results are normalized by being divided by the sum of similarities. These
functions follow a very standard item-to-item implementation as described in this paper: 

http://files.grouplens.org/papers/www10_sarwar.pdf

These prediction results are stored in a PredictiveRating model in a similar way to the similarity score, and can be
stored permanently; an nice upside that memory based collaborative filtering approaches don't have. The rest of the 
application logic is there to support web application features including the following:

- Task queue system
- Authentication services
- Recommendation system
- Predictive ratings
- Populating the models
- Setting up proper relationships
- UI Templating
- Jquery & Ajax submissions
- REST API for GET/POST requests

## Run Program

Inside of the project root `/path/to/folder/nominate`, run the following below:

### Installation
- `$ pip3 install -e .`
- `$ pip install -r requirements.txt`
- `$ yarn install`
- `$ bower install`

### Start up app and Task queues

- `$ flask run`
- `$ celery -A nominate.celery worker` / you want to kill celery workers: `$ pkill -f "celery worker"`
- `$ redis-server /usr/local/etc/redis.conf`
- Type in `http://127.0.0.1:5000/` in your browser.

## Package Contents:
.
├── README.md
├── __pycache__
│   └── config.cpython-36.pyc
├── bower.json
├── celery
├── config.py
├── gulpfile.js
├── node_modules [391 entries exceeds filelimit, not opening dir]
├── nominate
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── database.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   ├── similarity.cpython-36.pyc
│   │   ├── utilities.cpython-36.pyc
│   │   └── views.cpython-36.pyc
│   ├── database.py
│   ├── models.py
│   ├── nominate.db
│   ├── similarity.py
│   ├── static
│   │   ├── bower_components
│   │   │   ├── bootstrap
│   │   │   │   ├── CHANGELOG.md
│   │   │   │   ├── Gemfile
│   │   │   │   ├── Gemfile.lock
│   │   │   │   ├── Gruntfile.js
│   │   │   │   ├── ISSUE_TEMPLATE.md
│   │   │   │   ├── LICENSE
│   │   │   │   ├── README.md
│   │   │   │   ├── bower.json
│   │   │   │   ├── dist
│   │   │   │   │   ├── css
│   │   │   │   │   │   ├── bootstrap-theme.css
│   │   │   │   │   │   ├── bootstrap-theme.css.map
│   │   │   │   │   │   ├── bootstrap-theme.min.css
│   │   │   │   │   │   ├── bootstrap-theme.min.css.map
│   │   │   │   │   │   ├── bootstrap.css
│   │   │   │   │   │   ├── bootstrap.css.map
│   │   │   │   │   │   ├── bootstrap.min.css
│   │   │   │   │   │   └── bootstrap.min.css.map
│   │   │   │   │   ├── fonts
│   │   │   │   │   │   ├── glyphicons-halflings-regular.eot
│   │   │   │   │   │   ├── glyphicons-halflings-regular.svg
│   │   │   │   │   │   ├── glyphicons-halflings-regular.ttf
│   │   │   │   │   │   ├── glyphicons-halflings-regular.woff
│   │   │   │   │   │   └── glyphicons-halflings-regular.woff2
│   │   │   │   │   └── js
│   │   │   │   │       ├── bootstrap.js
│   │   │   │   │       ├── bootstrap.min.js
│   │   │   │   │       └── npm.js
│   │   │   │   ├── fonts
│   │   │   │   │   ├── glyphicons-halflings-regular.eot
│   │   │   │   │   ├── glyphicons-halflings-regular.svg
│   │   │   │   │   ├── glyphicons-halflings-regular.ttf
│   │   │   │   │   ├── glyphicons-halflings-regular.woff
│   │   │   │   │   └── glyphicons-halflings-regular.woff2
│   │   │   │   ├── grunt
│   │   │   │   │   ├── bs-commonjs-generator.js
│   │   │   │   │   ├── bs-glyphicons-data-generator.js
│   │   │   │   │   ├── bs-lessdoc-parser.js
│   │   │   │   │   ├── bs-raw-files-generator.js
│   │   │   │   │   ├── change-version.js
│   │   │   │   │   ├── configBridge.json
│   │   │   │   │   ├── npm-shrinkwrap.json
│   │   │   │   │   └── sauce_browsers.yml
│   │   │   │   ├── js
│   │   │   │   │   ├── affix.js
│   │   │   │   │   ├── alert.js
│   │   │   │   │   ├── button.js
│   │   │   │   │   ├── carousel.js
│   │   │   │   │   ├── collapse.js
│   │   │   │   │   ├── dropdown.js
│   │   │   │   │   ├── modal.js
│   │   │   │   │   ├── popover.js
│   │   │   │   │   ├── scrollspy.js
│   │   │   │   │   ├── tab.js
│   │   │   │   │   ├── tooltip.js
│   │   │   │   │   └── transition.js
│   │   │   │   ├── less [42 entries exceeds filelimit, not opening dir]
│   │   │   │   ├── nuget
│   │   │   │   │   ├── MyGet.ps1
│   │   │   │   │   ├── bootstrap.less.nuspec
│   │   │   │   │   └── bootstrap.nuspec
│   │   │   │   ├── package.js
│   │   │   │   └── package.json
│   │   │   ├── jquery
│   │   │   │   ├── AUTHORS.txt
│   │   │   │   ├── LICENSE.txt
│   │   │   │   ├── README.md
│   │   │   │   ├── bower.json
│   │   │   │   ├── dist
│   │   │   │   │   ├── core.js
│   │   │   │   │   ├── jquery.js
│   │   │   │   │   ├── jquery.min.js
│   │   │   │   │   ├── jquery.min.map
│   │   │   │   │   ├── jquery.slim.js
│   │   │   │   │   ├── jquery.slim.min.js
│   │   │   │   │   └── jquery.slim.min.map
│   │   │   │   ├── external
│   │   │   │   │   └── sizzle
│   │   │   │   │       ├── LICENSE.txt
│   │   │   │   │       └── dist
│   │   │   │   │           ├── sizzle.js
│   │   │   │   │           ├── sizzle.min.js
│   │   │   │   │           └── sizzle.min.map
│   │   │   │   └── src [34 entries exceeds filelimit, not opening dir]
│   │   │   └── react
│   │   │       ├── LICENSE
│   │   │       ├── PATENTS
│   │   │       ├── bower.json
│   │   │       ├── react-dom-server.js
│   │   │       ├── react-dom-server.min.js
│   │   │       ├── react-dom.js
│   │   │       ├── react-dom.min.js
│   │   │       ├── react-with-addons.js
│   │   │       ├── react-with-addons.min.js
│   │   │       ├── react.js
│   │   │       └── react.min.js
│   │   ├── css
│   │   │   ├── signup.css
│   │   │   └── style.css
│   │   ├── images
│   │   │   ├── favicon.ico
│   │   │   ├── logo.png
│   │   │   ├── movies [100 entries exceeds filelimit, not opening dir]
│   │   │   ├── search-icon.png
│   │   │   └── user-icon.png
│   │   └── scripts
│   │       ├── js
│   │       │   └── main.js
│   │       └── jsx
│   │           └── main.js
│   ├── templates
│   │   ├── about.html
│   │   ├── dashboard.html
│   │   ├── error.html
│   │   ├── index.html
│   │   ├── movie.html
│   │   ├── movies.html
│   │   ├── results.html
│   │   ├── signin.html
│   │   └── signup.html
│   ├── utilities.py
│   └── views.py
├── nominate.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── requires.txt
│   └── top_level.txt
├── package.json
├── requirements.txt
├── setup.py
├── yarn-error.log
└── yarn.lock


Libraries Used:

- Flask 0.12.2
- python 3.6.3
- numpy 1.13.3
- SQL-Alchemy
- yarn 1.3.2
- npm 5.5.1
- redis 4.0.2
- Celery 4.1.0
- SQLite format 3
- Bower 1.8.2

If you have any questions, please feel free to contact olsi.spahiu@ryerson.ca
