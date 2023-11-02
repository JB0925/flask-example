from unittest import mock

import pytest

from animals.animal_factory import AnimalFactory
from app import app
from pets.models import Pet
from test_utilities import use_database


@use_database
def test_pet_creation() -> None:
    app.testing = True
    data = {
        "name": "Tom",
        "age": 5,
        "species": "dog"
    }

    with app.test_client() as client:  # type: FlaskClient
        response = client.post("/pets", json=data)
        assert response.status_code == 201
        assert response.json["pet"]["name"] == data["name"]
        assert response.json["pet"]["age"] == data["age"]
        assert response.json["pet"]["species"] == 1  # Dog Enum value


@use_database
@mock.patch("app.Pet.create_pet", side_effect=Exception("Test Exception"))
def test_pet_creation_fails(mock_pet, capsys) -> None:
    app.testing = True
    data = {
        "name": "Tom",
        "age": 5,
        "species": "dog"
    }

    try:
        with app.test_client() as client:  # type: FlaskClient
            response = client.post("/pets", json=data)
            assert response.status_code == 400
            assert response.json["error"] == f"An error occurred when creating your pet: Test Exception"
    except Exception:
        capture = capsys.readouterr()
        assert "app.py::create_pet: Error trying to create a pet: Test Exception" in capture.out


@use_database
def test_get_pet() -> None:
    app.testing = True
    data = {
        "name": "Tom",
        "age": 5,
        "species": "dog"
    }

    Pet.create_pet(AnimalFactory().create_animal(**data))

    with app.test_client() as client:
        response = client.get("/pets/1")
        assert response.status_code == 200
        assert response.json["pet"]["name"] == data["name"]
        assert response.json["pet"]["age"] == data["age"]
        assert response.json["pet"]["species"] == 1


@use_database
@mock.patch("app.Pet.get_one_pet", side_effect=Exception("Test Exception"))
def test_get_one_pet_fails(mock_pet, capsys) -> None:
    app.testing = True

    try:
        with app.test_client() as client:  # type: FlaskClient
            response = client.pets("/pets/1")
            assert response.status_code == 400
            assert response.json["error"] == f"An error occurred when getting your pet: Test Exception"
            capture = capsys.readouterr()
            assert "app.py::get_one_pet: Error trying to get one pet: Test Exception" in capture.out
    except Exception as e:
        pass
