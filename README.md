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
stored permanently; an nice upside that memory based collaborative filtering approaches don't have. To run the 
recommendations, you must be logged in as the 'admin' user who's password is 'password'. From here, if you have the
redis application running on your host, as well as celery workers live, you'll be able to push a recommendation and 
prediction job on the task queue where the updating of the similarity, and prediction models is executed based on the 
latest ratings data.

The rest of the application logic is there to support web application features including the following:

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

Unzip cps842f17_prj_spahiu.zip
Go inside of the project root `/cps842f17_prj_spahiu` in a shell. 
Run the following below:

### First steps (assuming all dependencies are installed).

$ cd nominate 
$ export FLASK_APP=nominate
$ flask run

### Installation

- `$ pip3 install -r requirements.txt`
- `$ yarn install`
- `$ bower install`

### Start up app and Task queues

- `$ flask run`
- `$ celery -A nominate.celery worker` / you want to kill celery workers: `$ pkill -f "celery worker"`
- `$ redis-server /usr/local/etc/redis.conf`

Type in `http://127.0.0.1:5000/` in your browser to view the app.

## Package Contents:
.
├── README.md
├── bower.json
├── config.py
├── gulpfile.js
├── nominate
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── nominate.db
│   ├── similarity.py
│   ├── static
│   │   ├── css
│   │   │   ├── signup.css
│   │   │   └── style.css
│   │   ├── images
│   │   │   ├── favicon.ico
│   │   │   ├── logo.png
│   │   │   ├── movies
│   │   │   │   ├── [Many movie poster images]
│   │   │   ├── search-icon.png
│   │   │   └── user-icon.png
│   │   └── scripts
│   │       ├── js
│   │       │   └── main.js
│   │       └── jsx
│   │           └── main.js
│   ├── tasks.py
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
├── package.json
├── requirements.txt
├── setup.py
└── yarn.lock


## Libraries Used:

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
- pip3 9.0.1

If you have any questions, please feel free to contact olsi.spahiu@ryerson.ca
