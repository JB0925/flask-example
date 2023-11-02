import logging
import sys

from logging import Logger
from typing import Dict, List, Optional, Self, Union

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from animals.animal_types import ALL_PETS, AnimalType
from animals.simple_animal import Animal
from utils.errors import DatabaseNotConnectedError

logging.basicConfig(
   format='%(levelname)s - %(asctime)s: %(message)s ',
   level=logging.INFO,
   stream=sys.stdout
)

logger: Logger = logging.getLogger(__name__)

db: SQLAlchemy = SQLAlchemy()

def connect_db(app: Flask) -> None:
    """
    Connect to database and create tables
    if they do not already exist.
    """
    try:
        with app.app_context():
            db.app = app
            db.init_app(app)
            db.create_all()
    except Exception as e:
        message: str = (
            "models.py::connect_db - Failed to connect to database: "
            f"{e}"
        )
        logger.error(message, exc_info=True)

        raise DatabaseNotConnectedError(message)


class Pet(db.Model):
    """
    Generic class to write all pets
    to the database, and read from it as well.

    Attributes:
        id - int: The id of the pet.
        name - str: The name of the pet.
        age - int: The age of the pet.
        species - AnimalType: The species of the pet. Can only be one of the
        following: DOG, CAT, BIRD.
    """

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    species = db.Column(db.Integer, nullable=False)

    @staticmethod
    def _is_valid_pet_type(animal_type: AnimalType) -> bool:
        """
        Check if the animal type is a valid pet.
        """
        return animal_type in ALL_PETS

    @staticmethod
    def _validate(animal: Animal) -> bool:
        """
        Validate the input data.
        """
        if not Pet._is_valid_pet_type(animal.species):
            message: str = (
                f"Invalid species: {animal.species.name}. "
                f"Valid species are: {[pet.name for pet in ALL_PETS]}"
            )

            logger.error(message)
            raise TypeError(message)

        return True
    
    @staticmethod
    def create_pet(pet: Animal) -> Optional[Self]:
        """
        Create a pet in the database.

        @param name - str: The name of the pet.
        @param age - int: The age of the pet.
        @param species - AnimalType: The species of the pet. Can only be one of the
        following: DOG, CAT, BIRD.

        @return - Pet: The pet object that was created and added to the database.
        """
        Pet._validate(pet)  # will log and throw if not valid

        try:
            pet = Pet(name=pet.name, age=pet.age, species=pet.species.value)
            db.session.add(pet)
            db.session.commit()
            return pet
        except Exception as e:
            logger.error(f"Pet::create_pet - Failed to create pet: {e}", exc_info=True)
    
    @staticmethod
    def get_all_pets() -> List[Self]:
        """
        Get all pets from the database.

        @return - List[Pet]: A list of all pets in the database. If there is
        an error, return None.
        """
        try:
            return Pet.query.all()
        except Exception as e:
            logger.error(f"Pet::get_all_pets - Failed to get all pets: {e}", exc_info=True)
            return []
        
    @staticmethod
    def get_one_pet(id: int) -> Optional[Self]:
        """
        Get a single pet from the database.

        @param id - int: The id of the pet to get.

        @return - Pet: The pet object that was retrieved from the database.
        If there is an error, return None.

        NOTE: The use of the SQLAlchemy session "db" to query here is ok because,
        in the app.py file, we are using the app context to initialize the db.
        If it fails, an Exception will be thrown and caught in the app.py file.
        """
        try:
            return db.session.get(Pet, id)
        except Exception as e:
            logger.error(f"Pet::get_one_pet - Failed to get pet with id {id}: {e}", exc_info=True)
            return None
    
    @staticmethod
    def get_oldest_pet() -> Self:
        """
        Get the oldest pet.
        """
        pets: Self = Pet.query.all()
        if not pets:
            raise ValueError("No pets in the database.")
        
        return max(pets, key=lambda pet: pet.age)

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """
        Convert the pet object to a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "species": self.species
        }
    
    def __repr__(self) -> str:
        """
        Return a string representation of the pet object.
        """
        return f"<Pet {self.id}: Name: {self.name}, Age: {self.age}, Species Type: {self.species}>"
    
    def __str__(self) -> str:
        """
        Return a string representation of the pet object.
        """
        species_map: Dict[int, str] = {
            1: "dog",
            2: "cat",
            3: "bird"
        }
        return f"<Pet {self.name} is a {self.age} year old {species_map.get(self.species)}.>"
    
    def __eq__(self, other: Self) -> bool:
        """
        Check if two pet objects are equal.
        """
        return (
            self.id == other.id and
            self.name == other.name and
            self.age == other.age and
            self.species == other.species
        )
    
    def __sub__(self, other: Self) -> int:
        """
        Subtract the age of one pet from another.
        """
        return self.age - other.age
