from constants import Player


class Game:
    __curr_player: Player = None

    def __init__(self) -> None:
        self.__curr_player = Player.White

    def get_turn_checker(self) -> chr:
        return self.__curr_player.value

    def change_turn(self) -> None:
        self.__curr_player = (
            Player.Red if self.__curr_player == Player.White else Player.White
        )
