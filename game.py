from constants import Turn


class Game:

    __turn : Turn = None

    def __init__(self) -> None:
        self.__turn = Turn.White

    def get_turn_checker(self) -> chr:
        return self.__turn.value

    def change_turn(self) -> None:
        self.__turn = Turn.Red if self.__turn == Turn.White else Turn.White