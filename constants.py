# Author: Maciej Mucha

# constants.py - Plik przechowujący klasy i zmienne pomocnicze

from dataclasses import dataclass
from enum import Enum

# Czas zatrzymania programu po wizualizacji
sleep_time: int = 1
# Limit rekursji
recursion_limit = 100000


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


# Klasa przechowująca informację na temat oszacowywania rozmiaru drzewa mini-max
class Tree_size_test:
    call_counter: int = -1
    tree_range: list[int] = []
    max_depth: int = 0
    call_limit: int = 100000  # Limit wywołań
    tree_size: int = None


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
    random = "Losowy"
    suboptimal = "Suboptymalny"
    minimax = "Mini-max"


# Klasa reprezentująca kierunki ruchu graczy
class Directions:
    NW: Vector2 = Vector2(-1, -1)
    NE: Vector2 = Vector2(-1, 1)
    SW: Vector2 = Vector2(1, -1)
    SE: Vector2 = Vector2(1, 1)

    def get(self):
        return [self.NW, self.NE, self.SW, self.SE]


# EOF
