from functools import wraps
from typing import Callable

import pytest

from animals.animal_types import AnimalType
from animals.other_animals import Lion, Shark
from animals.simple_animal import Animal
from app import app
from pets.pets import Bird, Cat, Dog
from pets.models import Pet, db

@pytest.fixture
def use_database(func: Callable) -> Callable:
    """Decorator that clears the database before each test."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with app.app_context():
            db.drop_all()
            db.create_all()
            func(*args, **kwargs)
    return wrapper

@pytest.fixture
def valid_pets():
    """Create valid pets."""
    return [
        Dog("Fido", 5),
        Cat("Garfield", 3),
        Bird("Tweety", 1),
    ]

@pytest.fixture
def invalid_pets():
    """Create invalid pets."""
    return [
        Lion("Simba", 5),
        Shark("Jaws", 3),
    ]

@pytest.fixture
def types_to_validate():
    """Create types to validate."""
    return [
        {"name": "Fido", "age": 5, "species": "dog"},
        {"name": "Garfield", "age": 3, "species": "cat"},
        {"name": "Tweety", "age": 1, "species": "bird"},
        {"name": "Simba", "age": "5", "species": "lion"},
        {"name": 21, "age": 3, "species": AnimalType.SHARK},
        {"name": "Joe", "age": 10}
    ] 
