from typing import Dict, List, Union
from unittest import mock

import pytest

from app import app
from pets.models import Pet, connect_db
from pets.pets import Dog
from test_utilities import use_database
from utils.errors import DatabaseNotConnectedError
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
        with pytest.raises(Exception) as err:
            Pet.create_pet(animal)

        assert "Invalid species" in str(err.value)
        assert err.type == TypeError

    assert Pet.query.count() == 0

@use_database
@mock.patch("pets.models.db")
def test_pet_model_creation_fails_even_with_valid_type(mock_db, capsys) -> None:
    """
    Test that the Pet model cannot be created even with a valid type.
    This could occur because of a database issue, network issue, etc.

    NOTE: We need to mock the database session here because we are 
    trying to test what happens if there is an error with the database, etc.
    """
    pet = Dog(name="Fido", age=5)
    mock_db.session.add.side_effect = Exception('Mocked exception')

    try:
        Pet.create_pet(pet)
    
    except Exception as err:
        assert "Mocked exception" in str(err.value)
        assert err.type == Exception
        captured_text = capsys.readouterr()
        assert "Failed to create pet" in captured_text.out

    assert Pet.query.count() == 0


@use_database
@mock.patch("pets.models.db")
def test_database_setup_fails(mock_connect_db, capsys) -> None:
    mock_connect_db.init_app.side_effect = Exception('Mocked exception')

    try:
        connect_db(app)
    
    except Exception as err:
        print(err)
        assert type(err) == DatabaseNotConnectedError
        captured_text = capsys.readouterr()
        assert "Failed to connect to database" in captured_text.out


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
@mock.patch("pets.models.db")
def test_get_all_pets_fails(mock_db, capsys) -> None:
    """
    Test that the Pet model cannot return all pets.
    This could occur because of a database issue, network issue, etc.

    NOTE: We need to mock the database session here because we are 
    trying to test what happens if there is an error with the database, etc.
    """
    mock_db.session.query.side_effect = Exception('Mocked exception')

    try:
        Pet.get_all_pets()
    
    except Exception as err:
        assert "Mocked exception" in str(err.value)
        assert err.type == Exception
        captured_text = capsys.readouterr()
        assert "Failed to get all pets" in captured_text.out

    assert Pet.query.count() == 0


@use_database
@mock.patch("pets.models.db")
def test_get_one_pet_fails(mock_db, capsys) -> None:
    """
    Test that the Pet model cannot return a pet.
    This could occur because of a database issue, network issue, etc.

    NOTE: We need to mock the database session here because we are 
    trying to test what happens if there is an error with the database, etc.
    """
    mock_db.session.get.side_effect = Exception('Mocked exception')

    try:
        Pet.get_one_pet(1)
    
    except Exception as err:
        assert "Mocked exception" in str(err.value)
        assert err.type == Exception
        captured_text = capsys.readouterr()
        assert "Failed to get one pet with id" in captured_text.out

    assert Pet.query.count() == 0


@use_database
def test_no_pets_in_db_raises_value_error() -> None:
    """Test that no pets in the database raises a value error."""
    with pytest.raises(ValueError) as err:
        Pet.get_oldest_pet()

    assert "No pets in the database" in str(err.value)
    assert err.type == ValueError


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
@mock.patch("pets.models.Pet")
def test_get_all_pets_fails(mock_db, capsys) -> None:
    """
    Test that the Pet model cannot return all pets.
    This could occur because of a database issue, network issue, etc.

    NOTE: We need to mock the database session here because we are 
    trying to test what happens if there is an error with the database, etc.
    """
    mock_db.query.side_effect = Exception('Mocked exception')

    try:
         p = Pet.get_all_pets()
    
    except Exception as err:
        assert "Mocked exception" in str(err.value)
        assert err.type == Exception
        captured_text = capsys.readouterr()
        assert "Failed to get all pets" in captured_text.out
        assert p == []

    assert Pet.query.count() == 0


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


@use_database
def test_get_oldest_pet_succeeds(valid_pets) -> None:
    """Test that one pet can be fetched."""
    for animal in valid_pets:
        Pet.create_pet(animal)

    assert Pet.query.count() == 3

    pet: Pet = Pet.get_oldest_pet()
    assert pet is not None
    assert isinstance(pet, Pet)
    assert pet.name == "Fido"
    assert pet.age == 5
    assert pet.species == 1

def test_repr() -> None:
    """Test that the Pet model repr is accurate."""
    pet = Pet(name="Fido", age=5, species=1)
    pet.id = 1
    assert repr(pet) == "<Pet 1: Name: Fido, Age: 5, Species Type: 1>"

def test_str() -> None:
    """Test that the Pet model str is accurate."""
    pet = Pet(name="Fido", age=5, species=1)
    assert str(pet) == "<Pet Fido is a 5 year old dog.>"

def test_eq() -> None:
    """Test that the Pet model eq is accurate."""
    pet1 = Pet(name="Fido", age=5, species=1)
    pet2 = Pet(name="Fido", age=5, species=1)
    pet3 = Pet(name="Fido", age=5, species=2)
    assert pet1 == pet2
    assert pet1 != pet3

def test_sub() -> None:
    """Test that the Pet model sub is accurate."""
    pet1 = Pet(name="Fido", age=5, species=1)
    pet2 = Pet(name="Fido", age=10, species=1)
    assert pet2 - pet1 == 5
    assert pet1 - pet2 == -5
