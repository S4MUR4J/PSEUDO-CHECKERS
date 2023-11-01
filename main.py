import os
from types import NoneType

from algoritm import Algorithm
from checkboard import Checkboard
from game import Game
from ui import UI


def main() -> None:
    ui = UI()
    game = Game()
    checkboard = Checkboard(ui.read_checkboard_size())
    algorithm = Algorithm()

    ui.draw_checkboard(checkboard.board, checkboard.size)

    while True:
        quit = input("Q - wyjście: ")
        if quit.upper() == "Q":
            break

        os.system("cls")
        game.change_turn()
        result = algorithm.find_best_checker(
            checkboard.board, checkboard.size, game.curr_player
        )

        checkboard.move_checker(result[0], result[1], game.curr_player)
        ui.draw_checkboard(checkboard.board, checkboard.size)


if __name__ == "__main__":
    main()
