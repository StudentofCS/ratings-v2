"""Seed the movie rating database with data."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
from model import connect_to_db, db
from server import app

os.system("dropdb ratings")
os.system("createdb ratings")

connect_to_db(app)
app.app_context().push()
db.create_all()


movie_list = []
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
 
    
    for movie in movie_data: 
        title = movie.get("title", "")
        overview = movie.get("overview", "")
        release_date = movie.get("release_date", datetime.now())
        format = "%Y-%m-%d"
        modified_release_date = datetime.strptime(release_date, format)
        poster_path = movie.get("poster_path", "")
        created_movie = crud.create_movie(title, overview, modified_release_date, poster_path)
        movie_list.append(created_movie)

        
db.session.add_all(movie_list)
db.session.commit()        


for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'

    user = crud.create_user(email, password)
    db.session.add(user)

    

    for n in range(10):
        movie = choice(movie_list)
        rating = crud.create_rating(movie, user, randint(1, 5))
        db.session.add(rating)

db.session.commit()
   