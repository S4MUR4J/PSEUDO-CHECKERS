from dataclasses import dataclass
from enum import Enum


class Player(Enum):
    White: chr = "W"
    Red: chr = "R"
    Empty: chr = " "


@dataclass
class Vector2:
    x: int = None
    y: int = None
