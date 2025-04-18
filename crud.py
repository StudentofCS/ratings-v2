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


if __name__ == '__main__':
    from server import app
    connect_to_db(app)