# main.py | Author: Maciej Mucha

import random

from algoritm import minimax_algorithm
from constants import EnemyMode, Infinity, Player, Vector2
from game import Game
from ui import (
    end_simulation,
    generate_raport,
    get_float_input,
    get_int_input,
    get_int_to_mode_input,
    get_yes_no_input,
    visualization,
)


def __get_game_parameters() -> int | int | int | int | bool | float:
    minimax_depth = get_int_input("Prosze o podanie rozmiaru drzewa minimax: ")
    max_player_moves = get_int_input(
        "Prosze o podanie maksymalnej liczby ruchów jednego gracza: "
    )
    checkboard_size = get_int_input("Prosze o podanie rozmiaru szachownicy: ")
    enemy_mode = get_int_to_mode_input()
    with_visual = get_yes_no_input("Czy wykonać program z wizualizacją [T/N]: ")
    sleep_time = (
        get_float_input("Prosze o podanie czasu oczekiwania na kolejny ruch: ")
        if with_visual
        else 0
    )
    return (
        minimax_depth,
        max_player_moves,
        checkboard_size,
        enemy_mode,
        with_visual,
        sleep_time,
    )


def __minimax_move(game: Game, depth: int) -> (Vector2, Vector2):
    game_copy = game.deep_copy()
    _, move = minimax_algorithm(
        game=game_copy,
        depth=depth,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        maximazing=True,
    )
    return move


def __suboptimal_move(game: Game) -> (Vector2, Vector2):
    best_move = None
    max_rating = Infinity.minus

    game_copy = game.deep_copy()
    for move in game.all_possible_moves():
        game_inner = game_copy
        game_inner.play_turn(move[1], move[0])
        curr_rating = game_inner.get_rating()
        if curr_rating > max_rating:
            max_rating = curr_rating
            best_move = move

    return best_move


def __random_move(game: Game) -> (Vector2, Vector2):
    moves = game.all_possible_moves()

    if moves:
        move = random.choice(moves)
        return move


def __move_decider(game: Game, enemy_mode: EnemyMode, depth: int) -> (Vector2, Vector2):
    if game.curr_player == Player.White:
        return __minimax_move(game, depth)
    else:
        if enemy_mode == EnemyMode.random:
            return __random_move(game)

        elif enemy_mode == EnemyMode.suboptimal:
            return __suboptimal_move(game)
        else:
            return __minimax_move(game, depth)


def main() -> None:
    (
        minimax_depth,
        max_player_moves,
        board_size,
        enemy_mode,
        with_visual,
        sleep_time,
    ) = __get_game_parameters()

    game = Game(board_size)

    while True:
        if with_visual:
            visualization(
                board=game.board, board_size=game.board_size, sleep_time=sleep_time
            )
        if game.is_end_game:
            generate_raport(
                board_size,
                game.who_won,
                game.white_score,
                game.red_score,
                game.tour_count,
            )
            break

        move = __move_decider(game, enemy_mode, minimax_depth)
        if move:
            game.play_turn(move[1], move[0])
        else:
            break

    end_simulation()


if __name__ == "__main__":
    main()

# EOF
