from algoritm import Algorithm
from game import Game
from ui import UI


def main() -> None:
    ui = UI()
    game = Game(ui.checkboard_size)
    algorithm = Algorithm()

    while True:
        if ui.with_visualization:
            ui.visualization(
                board=game.board, board_size=game.board_size, who_won=game.who_won
            )

        if game.is_end_game:
            ui.generate_raport(board_size=game.board_size, who_won=game.who_won)
            break

        result = algorithm.find_best_checker(
            board=game.board, board_size=game.board_size, curr_player=game.curr_player
        )

        game.play_turn(old_pos=result[0], new_pos=result[1])


if __name__ == "__main__":
    main()
