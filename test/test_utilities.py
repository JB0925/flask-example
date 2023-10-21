from functools import wraps
from typing import Callable

from app import app
from pets.models import db


def use_database(func: Callable) -> Callable:
    """Decorator that clears the database before each test."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.app_context():
            db.drop_all()
            db.create_all()
            func(*args, **kwargs)
    return wrapper