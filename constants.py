from enum import Enum



class Tile(Enum):
    White = 'W'
    Red = 'R'
    Empty = ' '

class Turn(Enum):
    White = Tile.White.value
    Red = Tile.Red.value

class Vector2:
    
    x : int = None
    y : int = None

    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y