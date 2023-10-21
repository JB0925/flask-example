from animals.animal_types import AnimalType
from animals.simple_animal import Animal


class Shark(Animal):
    """
    Class to create a shark object.
    """
    def __init__(self, name: str, age: int):
        super().__init__(name, age, AnimalType.SHARK)

    def __str__(self) -> str:
        return f"{self.name} is a {self.age} year old shark."

    def speak(self) -> None:
        print("I'm a shark! I don't speak!")

    def do_stuff(self) -> None:
        print("I'm swimming and eating fish!")


class Lion(Animal):
    """
    Class to create a lion object.
    """
    def __init__(self, name: str, age: int):
        super().__init__(name, age, AnimalType.LION)

    def __str__(self) -> str:
        return f"{self.name} is a {self.age} year old lion."

    def speak(self) -> None:
        print("Roar!")

    def do_stuff(self) -> None:
        print("I'm roaring and eating meat!")
