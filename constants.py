from enum import Enum


class Player(Enum):
    White: chr = "W"
    Red: chr = "R"
    Empty: chr = " "


class Vector2:
    x: int = None
    y: int = None

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
