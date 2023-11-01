from typing import Generator, List

from _pytest.capture import CaptureFixture, CaptureResult

from animals.animal_types import AnimalType
from animals.simple_animal import Animal
from pets.pets import Bird, Cat, Dog


def test_pet_creation_no_db(
        valid_pets: List[Animal], 
        capsys: Generator[CaptureFixture[str], None, None]
) -> None:
    """
    Test that the Pet model can be created correctly.

    @param valid_pets: A list of valid pets (DOG, CAT, BIRD).
    @param capsys: Pytest fixture to capture stdout.
    @return: None.
    """
    dog: Dog = valid_pets[0]
    cat: Cat = valid_pets[1]
    bird: Bird = valid_pets[2]

    # Check that dogs are created correctly
    assert dog.name == "Fido"
    assert dog.age == 5
    assert dog.species == AnimalType.DOG
    dog.do_stuff()
    captured: CaptureResult[str] = capsys.readouterr()
    assert captured.out == "I'm playing and barking!\n"
    dog.speak()
    captured = capsys.readouterr()
    assert captured.out == "Woof!\n"
    assert str(dog) == "Fido is a 5 year old dog."
    assert isinstance(dog, Animal) and isinstance(dog, Dog)

    # And cats
    assert cat.name == "Garfield"
    assert cat.age == 3
    assert cat.species == AnimalType.CAT
    cat.do_stuff()
    captured = capsys.readouterr()
    assert captured.out == "I'm playing and meowing!\n"
    cat.speak()
    captured = capsys.readouterr()
    assert captured.out == "Meow!\n"
    assert str(cat) == "Garfield is a 3 year old cat."
    assert isinstance(cat, Animal) and isinstance(cat, Cat)

    # And birds
    assert bird.name == "Tweety"
    assert bird.age == 1
    assert bird.species == AnimalType.BIRD
    bird.do_stuff()
    captured = capsys.readouterr()
    assert captured.out == "I'm flying and chirping!\n"
    bird.speak()
    captured = capsys.readouterr()
    assert captured.out == "Chirp chirp!\n"
    assert str(bird) == "Tweety is a 1 year old bird."
    assert isinstance(bird, Animal) and isinstance(bird, Bird)
