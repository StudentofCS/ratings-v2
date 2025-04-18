"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/movies')
def all_movies():
    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)


@app.route('/movies/<movie_id>')
def get_movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template('movie_details.html', movie=movie)


@app.route('/users')
def all_users():
    users = crud.get_users()
    return render_template('all_users.html', users=users)


@app.route('/user/<user_id>')
def get_user(user_id):
    user = crud.get_user_by_id(user_id)

    return render_template('user_profile.html', user=user)


if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)
