from dataclasses import dataclass
from enum import Enum

sleep_time: int = 1
recursion_limit = 100000


@dataclass
class Vector2:
    x: int
    y: int


@dataclass
class Infinity:
    minus: float = float("-inf")
    plus: float = float("inf")


class Tree_size_test:
    call_counter: int = -1
    tree_range: list[int] = []
    max_depth: int = 0
    call_limit: int = 100000
    tree_size: int = None


class Player(Enum):
    White = "W"
    Red = "R"
    Empty = " "


class Points(Enum):
    Capture = 1
    King = 3


class EnemyMode(Enum):
    random = "Random"
    suboptimal = "Suboptimal"
    minimax = "Mini-max"


class Directions:
    NW: Vector2 = Vector2(-1, -1)
    NE: Vector2 = Vector2(-1, 1)
    SW: Vector2 = Vector2(1, -1)
    SE: Vector2 = Vector2(1, 1)

    def get(self):
        return [self.NW, self.NE, self.SW, self.SE]
