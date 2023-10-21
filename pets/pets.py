from animals.animal_types import AnimalType
from animals.simple_animal import Animal


class Dog(Animal):
    """
    Class to create a dog object.
    """
    def __init__(self, name: str, age: int):
        super().__init__(name, age, AnimalType.DOG)

    def __str__(self) -> str:
        return f"{self.name} is a {self.age} year old dog."

    def speak(self) -> None:
        print("Woof!")

    def do_stuff(self) -> None:
        print("I'm playing and barking!")


class Cat(Animal):
    """
    Class to create a cat object.
    """
    def __init__(self, name: str, age: int):
        super().__init__(name, age, AnimalType.CAT)

    def __str__(self) -> str:
        return f"{self.name} is a {self.age} year old cat."

    def speak(self) -> None:
        print("Meow!")

    def do_stuff(self) -> None:
        print("I'm playing and meowing!")


class Bird(Animal):
    """
    Class to create a bird object.
    """
    def __init__(self, name: str, age: int):
        super().__init__(name, age, AnimalType.BIRD)

    def __str__(self) -> str:
        return f"{self.name} is a {self.age} year old bird."

    def speak(self) -> None:
        print("Chirp chirp!")

    def do_stuff(self) -> None:
        print("I'm flying and chirping!")
