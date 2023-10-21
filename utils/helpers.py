import os

from logging import Logger
from typing import Dict, List, Optional, Tuple, Union

from flask import Flask

from utils.errors import (
    EnvironmentNotSetError,
    InvalidRequestBodyError, 
    InvalidTypesError
)


def check_for_correct_types(name: str, age: int, species: str) -> bool:
    """
    A simple check on the types passed in via the request.

    @param name - str: The name of the animal.
    @param age - int: The age of the animal.
    @param species - str: The species of the animal.

    @return bool: True if all types are correct, False otherwise.
    """
    params_and_types: List[Tuple[str, Union[str, int]]] = [
        (name, str),
        (age, int),
        (species, str)
    ]

    return all(
        isinstance(param, param_type) 
        for param, param_type in params_and_types
    )

def validate_json(
        data: Dict[str, Union[str, int]],
        logger: Logger
) -> None:
    """
    Simple validation on incoming json data on POST requests.
    Checks that each field exists and is the correct type.

    @param data - Dict[str, Union[str, int]]: The json data to validate.
    @param logger - Logger: The logger to use for logging errors.

    @return None
    """
    name: Optional[str] = data.get('name')
    age: Optional[int] = data.get('age')
    species: Optional[str] = data.get('species')

    if any(n is None for n in (name, age, species)):
        message: str = (
            "helpers.py::validate_json - "
            "One or more of the following values are missing: "
            "name, age, species. Your provided values are: "
            f"name={name}, age={age}, species={species}"
        )

        logger.error(message)
        raise InvalidRequestBodyError(message)

    if not check_for_correct_types(name, age, species):
        message: str = (
            "helpers.py::validate_json - "
            "One or more of the following values are of the wrong type: "
            "name, age, species. Your provided values are: "
            f"name={name} of type {type(name)}, age={age} of type {type(age)}, "
            f"species={species} of type {type(species)}."
        )

        logger.error(message)
        raise InvalidTypesError(message)
    
def configure_app(app: Flask) -> None:
    """
    Configure the Flask app and SQLAlchemy.
    """
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']: bool = False
    app.config['SQLALCHEMY_ECHO']: bool = False
    app.config['SECRET_KEY']: str = get_flask_secret()
    app.config['SQLALCHEMY_DATABASE_URI']: str = get_database_uri()

def get_database_uri() -> str:
    """
    Get the database URI from the environment variable.
    If not set, raise an EnvironmentNotSetError.

    @return str: The database URI.
    """
    database_uri: Optional[str] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    if database_uri is None:
        raise EnvironmentNotSetError("SQLALCHEMY_DATABASE_URI is not set.")
    
    return database_uri

def get_flask_secret() -> str:
    """
    Get the flask secret key from the environment variable.
    If not set, raise an EnvironmentNotSetError.

    @return str: The flask secret key.
    """
    secret_key: Optional[str] = os.environ.get('SECRET_KEY')
    if secret_key is None:
        raise EnvironmentNotSetError("SECRET_KEY is not set.")

    return secret_key
