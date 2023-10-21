from abc import ABC, abstractmethod

from animals.animal_types import AnimalType


class Animal(ABC):
    """
    Generic template class to create animals.

    NOTE: Anything with @abstractmethod needs to be implemented
    in the child class, otherwise an error will be thrown.
    """
    def __init__(self, name: str, age: int, species: AnimalType):
        self.name: str = name
        self.age: int = age
        self.species: AnimalType = species

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def speak(self) -> None:
        """
        Print a message to the console, i.e "Woof!"
        for a dog, "Meow!" for a cat, etc.
        """
        pass

    @abstractmethod
    def do_stuff(self) -> None:
        """
        Print a message to the console, i.e "I'm playing!" or
        "I'm roaring!" or "I'm flying!" etc.
        """
        pass
