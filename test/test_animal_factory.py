import pytest

from animals.animal_factory import AnimalFactory
from animals.simple_animal import Animal
from utils.constants import Constants
from animals.other_animals import Lion, Shark
from pets.pets import Bird, Cat, Dog


@pytest.mark.parametrize("name, age, species, expected", [
    ("Tom", 5, Constants.DOG, Dog),
    ("Tom", 5, Constants.CAT, Cat),
    ("Tom", 5, Constants.BIRD, Bird),
    ("Tom", 5, Constants.SHARK, Shark),
    ("Tom", 5, Constants.LION, Lion),
])
def test_animal_factory(name, age, species, expected) -> None:
    factory: AnimalFactory = AnimalFactory()
    for _ in range(5):
        animal: Animal = factory.create_animal(name, age, species)
        assert isinstance(animal, expected)
        assert animal.name == name
        assert animal.age == age
        assert animal.species.name == species
