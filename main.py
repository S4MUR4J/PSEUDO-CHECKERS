from algoritm import Algorithm
from checkboard import Checkboard
from game import Game
from ui import UI


def main() -> None:
    ui = UI()
    game = Game()
    checkboard = Checkboard(ui.checkboard_size)
    algorithm = Algorithm()

    while True:
        if ui.with_visualization:
            ui.visualization(checkboard.board, checkboard.size, game.is_end_game)

        if game.is_end_game:
            ui.generate_raport()
            break

        game.change_turn()
        result = algorithm.find_best_checker(
            checkboard.board, checkboard.size, game.curr_player
        )

        checkboard.move_checker(result[0], result[1], game.curr_player)
        game.update_who_won(checkboard.board, checkboard.size)


if __name__ == "__main__":
    main()
