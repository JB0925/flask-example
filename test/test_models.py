from typing import Dict, List, Union

import pytest

from app import app
from pets.models import Pet
from test_utilities import use_database
from utils.helpers import configure_app

configure_app(app)

@use_database
def test_pet_model_creation_succeeds(valid_pets) -> None:
    """Test that the Pet model can be created."""
    for animal in valid_pets:
        Pet.create_pet(animal)

    assert Pet.query.count() == 3


@use_database
def test_pet_model_creation_fails(invalid_pets) -> None:
    """Test that the Pet model cannot be created."""
    for animal in invalid_pets:
        with pytest.raises(TypeError) as err:
            Pet.create_pet(animal)

        assert "Invalid species" in str(err.value)

    assert Pet.query.count() == 0


@use_database
def test_get_all_pets_succeeds(valid_pets) -> None:
    """Test that the Pet model can be created."""
    for animal in valid_pets:
        Pet.create_pet(animal)

    assert Pet.query.count() == 3

    pets = Pet.get_all_pets()

    assert len(pets) == 3
    assert all(isinstance(p, Pet) for p in pets)

@use_database
def test_get_one_pet_succeeds(valid_pets) -> None:
    """Test that one pet can be fetched."""
    for animal in valid_pets:
        Pet.create_pet(animal)

    assert Pet.query.count() == 3

    pets: List[Pet] = Pet.get_all_pets()
    pet: Pet = pets[0]
    same_pet: Pet = Pet.get_one_pet(pet.id)
    assert same_pet is not None
    assert isinstance(same_pet, Pet)
    assert same_pet.name == pet.name
    assert same_pet.age == pet.age
    assert same_pet.species == pet.species


@use_database
def test_pet_is_converted_to_dictionary(valid_pets) -> None:
    """Test that a pet can be converted to a dictionary."""
    for animal in valid_pets:
        Pet.create_pet(animal)

    assert Pet.query.count() == 3

    pets: List[Pet] = Pet.get_all_pets()
    pet: Pet = pets[0]
    pet_dict: Dict[str, Union[str, int]] = pet.to_dict()

    assert isinstance(pet_dict, dict)
    assert pet_dict['name'] == pet.name
    assert pet_dict['age'] == pet.age
    assert pet_dict['species'] == pet.species
