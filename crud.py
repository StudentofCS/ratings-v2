"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie


def create_rating(movie, user, score):
    """Create and return a movie rating."""

    movie_rating = Rating(movie=movie, user=user, score=score)

    return movie_rating

def get_movies():
    """Return a list of all the movies."""
    movies = db.session.query(Movie).all()
    return movies


def get_movie_by_id(id):
    movie = db.session.query(Movie).filter(Movie.movie_id == id).one()

    # movie = Movie.query.get(id)
    return movie


def get_users():
    """Return a list of all the users."""
    return db.session.query(User).all()


def get_user_by_id(id):
    """Return user by their id."""
    return db.session.query(User).filter(User.user_id == id).one()


def get_user_by_email(email):
    """Return user id from user email. Return None if email not found"""
    return db.session.query(User).filter(User.email == email).first()
    # user = User.query.get(email)
    # print(user)
    # return User.query.get(email)

def get_movies_by_term(term):
    term_string = f'%{term}%'
    # print(term_string)
    return db.session.query(Movie.title).filter(Movie.title.like(term_string)).all()


def get_movie_by_title(title):
    """Return movie by it's title."""
    return db.session.query(Movie).filter(Movie.title == title).first()


def get_user_ratings(user):
    """Return all the ratings a user has made."""
    return db.session.query(Rating).filter(Rating.user_id == user.user_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)