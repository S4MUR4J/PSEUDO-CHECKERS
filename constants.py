# constants.py | Author: Maciej Mucha

# Plik przechowujący klase pomocnicze

from dataclasses import dataclass
from enum import Enum


# Klasa przechowująca pozycję na planszy X | Y
@dataclass
class Vector2:
    x: int
    y: int


# Klasa przechowująca wartość minimalną i maksymalną float
@dataclass
class Infinity:
    minus: float = float("-inf")
    plus: float = float("inf")


# Enum reprezentujący rodzaje gracza na planszy
class Player(Enum):
    White = "W"
    Red = "R"
    Empty = " "


# Enum przechowujący punktacje za ruchy
class Points(Enum):
    Capture = 1
    King = 3


# Enum reprezentujący rodzaje trybów podejmowania decyzji przeciwnika
class EnemyMode(Enum):
    random = "1"
    suboptimal = "2"
    minimax = "3"


# Klasa reprezentująca kierunki ruchu graczy
class Directions:
    NW: Vector2 = Vector2(-1, -1)
    NE: Vector2 = Vector2(-1, 1)
    SW: Vector2 = Vector2(1, -1)
    SE: Vector2 = Vector2(1, 1)

    def get(self):
        return [self.NW, self.NE, self.SW, self.SE]


# EOF
