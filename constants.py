from dataclasses import dataclass
from enum import Enum


class Player(Enum):
    White = "W"
    Red = "R"
    Empty = " "


@dataclass
class Vector2:
    x: int
    y: int
