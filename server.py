"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, 
                   redirect, jsonify)
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    if "user_id" in session:
        return redirect(f"/user/{session['user_id']}")
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


@app.route('/users', methods=['POST'])
def create_new_user():
    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)
    print(user)
    if user != None:
        flash('User is already registered')
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully")
    return redirect("/")

    
@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    user = crud.get_user_by_email(email)

    if user.email == email:
        if user.password == password:
            session['user_id'] = session.get('user_id', user.user_id)
            session['user'] = user
            flash("Logged in!")
            return redirect(f"/user/{session['user_id']}")
        else:
            flash("Incorrect password!")
            return redirect("/")
    else:
        flash("User not found in our database")
        return redirect("/"), 404


@app.route('/search', methods=['POST'])
def search_movies():
    term = request.form['movie_search']
    movie_list = crud.get_movies_by_term(term)
    user = crud.get_user_by_id(session['user_id'])
    return render_template('user_profile.html', movie_list=movie_list, user=user)
 
        

@app.route("/rate", methods=['POST'])
def make_ratings():
    selected_movie_titles = request.form.getlist("movie")
    print(selected_movie_titles)
    
    ratings = []   
    user = crud.get_user_by_id(session['user_id'])
    for movie_title in selected_movie_titles:
        movie = crud.get_movie_by_title(movie_title)
        score = request.form[movie_title]
        rating = crud.create_rating(movie=movie, user=user, score=score)
        ratings.append(rating)

    db.session.add_all(ratings)
    db.session.commit()

    user_ratings = crud.get_user_ratings(user)
    return render_template('user_profile.html', user=user, user_ratings=user_ratings)    
    
if __name__ == "__main__":

    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, port=6060)
