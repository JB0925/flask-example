from enum import Enum
from typing import Final, Set


class AnimalType(Enum):
    DOG: int = 1
    CAT: int = 2
    BIRD: int = 3
    SHARK: int = 4
    LION: int = 5

ALL_PETS: Final[Set[AnimalType]] = {
    AnimalType.DOG,
    AnimalType.CAT,
    AnimalType.BIRD
}
