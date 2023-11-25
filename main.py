# Author: Maciej Mucha

# main.py - Realizacja sterowania nad symulacją

from constants import EnemyMode, Infinity, Player, Vector2
from game import Game
from method import minimax_algorithm, random_move, suboptimal_move
from ui import *


# Funkcja zwracająca parametry symulacji na podstawie decyzji uzytkownika
def __get_game_parameters() -> int | int | int | int | bool | float:
    minimax_depth = get_int_input("Prosze o podanie rozmiaru drzewa minimax: ")
    max_player_moves = get_int_input(
        "Prosze o podanie maksymalnej liczby ruchów jednego gracza: "
    )
    checkboard_size = get_int_input("Prosze o podanie rozmiaru szachownicy: ")
    enemy_mode = get_int_to_mode_input()
    with_visual = get_yes_no_input("Czy wykonać program z wizualizacją [T/N]: ")
    return (minimax_depth, max_player_moves, checkboard_size, enemy_mode, with_visual)


# Funkcja zwracająca najlepszy ruch wyznaczony przy uzyciu algorytmu minimax
def __minimax_move(game: Game, depth: int) -> (Vector2, Vector2):
    game_copy = game.deep_copy()
    _, move = minimax_algorithm(
        game=game_copy,
        depth=depth,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        max_player=game.curr_player,
    )
    return move


# Funkcja dobierająca odpowiednia metode wyznaczenia ruchu na podstawie
# tego, ktorego gracza jest tura i parametrów symulacji
def __move_decider(game: Game, enemy_mode: EnemyMode, depth: int) -> (Vector2, Vector2):
    if game.curr_player == Player.White:
        return __minimax_move(game, depth)
    else:
        if enemy_mode == EnemyMode.random:
            return random_move(game)

        elif enemy_mode == EnemyMode.suboptimal:
            return suboptimal_move(game.deep_copy())
        else:
            return __minimax_move(game, depth)


def main() -> None:
    (
        minimax_depth,
        max_player_moves,
        board_size,
        enemy_mode,
        with_visual,
    ) = __get_game_parameters()  # Wczytanie potrzebnych parametrów

    game = Game(board_size, max_player_moves)  # Stworzenie instancji gry

    # Pętla symulacji kończy się wraz z zakończeniem gry
    while True:
        # Wykonanie wizualizacji zgodnie z parametrem
        if with_visual:
            visualization(
                board=game.board, board_size=board_size, move=game.move_history[-1]
            )
        # Na koniec gry generowany jest raport
        if game.is_end_game:
            generate_raport(
                board_size=board_size,
                white_score=game.white_score,
                red_score=game.red_score,
                move_history=game.move_history,
            )
            break

        # Ruch wybierany na podstawie parametrów i aktualnego gracza
        move = __move_decider(game, enemy_mode, minimax_depth)
        if move:
            game.play_turn(move[1], move[0])

    # Komunikat o końcu programu
    end_simulation()


if __name__ == "__main__":
    main()

# EOF
