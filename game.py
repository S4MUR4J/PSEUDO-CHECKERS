from constants import Player


class Game:
    curr_player: Player = None

    def __init__(self) -> None:
        self.curr_player = Player.White

    def change_turn(self) -> None:
        self.curr_player = (
            Player.Red if self.curr_player == Player.White else Player.White
        )
