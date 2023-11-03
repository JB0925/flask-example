from animals.other_animals import Lion, Shark
from animals.simple_animal import Animal
from pets.pets import Bird, Cat, Dog
from utils.constants import Constants


class AnimalFactory:
    """
    Factory to create an animal based on the type.
    """
    def __init__(self) -> None:
        pass

    def create_animal(
            self,
            name: str,
            age: int,
            species: str
    ) -> Animal:
        """
        Create an Animal based on the species.

        @param name - str: The name of the animal.
        @param age - int: The age of the animal.
        @param species - str: The species of the animal.

        @return Animal: The animal object.
        """
        match species.upper():
            case Constants.DOG:
                return Dog(name, age)
            case Constants.CAT:
                return Cat(name, age)
            case Constants.BIRD:
                return Bird(name, age)
            case Constants.SHARK:
                return Shark(name, age)
            case Constants.LION:
                return Lion(name, age)
            case _:
                raise ValueError(f"Unknown animal type: {species.name}")
