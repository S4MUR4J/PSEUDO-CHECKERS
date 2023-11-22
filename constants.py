from dataclasses import dataclass
from enum import Enum


@dataclass
class Mode:
    order: int
    message: str


@dataclass
class Vector2:
    x: int
    y: int


@dataclass
class Infinity:
    minus: float = float("-inf")
    plus: float = float("inf")


class Player(Enum):
    White = "W"
    Red = "R"
    Empty = " "


class EnemyMode(Enum):
    random = Mode(1, "1. Losowy")
    suboptimal = Mode(2, "Suboptymalny")
    minimax = Mode(3, "Mini-max")


class Directions:
    NW: Vector2 = Vector2(-1, -1)
    NE: Vector2 = Vector2(-1, 1)
    SW: Vector2 = Vector2(1, -1)
    SE: Vector2 = Vector2(1, 1)

    def get(self):
        return [self.NW, self.NE, self.SW, self.SE]
