import logging
import sys

from logging import Logger
from typing import Dict, List, Union

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from animals.animal_factory import AnimalFactory
from animals.simple_animal import Animal
from pets.models import Pet, connect_db
from utils.helpers import configure_app, validate_json


logging.basicConfig(
   format='%(levelname)s - %(asctime)s: %(message)s ',
   level=logging.INFO,
   stream=sys.stdout
)

logger: Logger = logging.getLogger(__name__)

app: Flask = Flask(__name__)
load_dotenv()
configure_app(app)
connect_db(app)

factory: AnimalFactory = AnimalFactory()

@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id: int):
    """
    Get a pet from the database
    with the given id as a key.
    """
    try:
        pet: Pet = Pet.query.get(id)
        return jsonify(pet=pet.to_dict())
    except Exception as e:
        logger.error(f"app.py::get_pet: Error trying to get one pet: {e}", exc_info=True)

@app.route('/pets', methods=['GET'])
def get_pets():
    """
    Get a list of pet objects from the database.
    """
    try:
        pets: List[Animal] = Pet.get_all_pets()
        return jsonify(pets=[p.to_dict() for p in pets])
    except Exception as e:
        logger.error(f"app.py::get_pets: Error trying to get all pets: {e}", exc_info=True)

@app.route('/pets', methods=['POST'])
def create_pet():
    """
    Create a pet and write it to the database.
    """
    try:
        data: Dict[str, Union[int, str]] = request.json
        validate_json(data, logger)

        animal: Animal = factory.create_animal(**data)
        pet: Animal = Pet.create_pet(animal)  # stores in db and returns pet object
        return jsonify(pet=pet.to_dict()), 201
    except Exception as e:
        logger.error(f"app.py::create_pet: Error trying to create a pet: {e}", exc_info=True)
        return jsonify(error=f"An error occurred when creating your pet: {e}"), 400
