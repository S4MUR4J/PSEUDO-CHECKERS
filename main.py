import random

from algoritm import Algorithm
from game import Game
from ui import UI


def main() -> None:
    ui = UI()
    game = Game(ui.checkboard_size)

    while True:
        if ui.with_visualization:
            ui.visualization(
                board=game.board,
                board_size=game.board_size,
            )

        if game.is_end_game:
            ui.generate_raport(
                board_size=game.board_size,
                who_won=game.who_won,
                white_score=game.white_score,
                red_score=game.red_score,
                tour_count=game.tour_count,
            )
            break

        # ? SIMULATE PART

        moves = game.all_possible_moves()

        if moves:
            move = random.choice(moves)
            new_pos = move[0]
            old_pos = move[1]
            game.play_turn(old_pos, new_pos)
        else:
            continue

        # ? END SIMULATE PART


if __name__ == "__main__":
    main()
