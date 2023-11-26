# Author: Maciej Mucha

# method.py - Realizacja zadanej metody sztucznej inteligencji mini-max
# oraz funkcji znajdowania suboptymalnego i losowego ruchu

import random

from constants import Infinity, Player, Tree_size_test, Vector2
from game import Game


def minimax_algorithm(
    game: Game, depth: int, alpha: int, beta: int, max_player: bool
) -> int | Vector2:
    # Sprawdzenie czy gra została skończona
    if depth == 0 or game.is_end_game:
        return (
            game.get_player_rating(game.curr_player),
            None,
        )  # Ocena stanu gry dla gracza maksymalizującego, bez najlepszego ruchu

    best_move = None

    # Sprawdzanie na gracza maksymalizującego
    if max_player:
        max_rating = (
            Infinity.minus
        )  # Dla początku rozpatrywania drzewa nieosiągalna wartość

        # Rozpatrywanie każdego możliwego ruchu z danego stanu gry
        for move in game.all_possible_moves():
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])  # Wykonanie ruchu na kopii
            rating, _ = minimax_algorithm(
                game=game_copy,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
                max_player=False,
            )  # Rozpatrzenie stanu gry po wykonanym ruchu
            # Czy jest to do tej pory najlepszy stan gry dla gracza
            if rating > max_rating:
                max_rating = rating
                best_move = move
            alpha = max(alpha, rating)  # Podmiana alfy gdy większa niż dotychczas
            # Cięcie alfa-beta
            if beta <= alpha:
                break
        return max_rating, best_move  # Zwraca największą ocenę i najlepszy ruch gracza

    # Sprawdzenie dla gracza minimalizującego
    else:
        min_rating = (
            Infinity.plus
        )  # Dla początku rozpatrywania drzewa nieosiągalna wartość

        # Rozpatrywanie każdego możliwego ruchu z danego stanu gry
        for move in game.all_possible_moves():
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])  # Wykonanie ruchu na kopii
            rating, _ = minimax_algorithm(
                game=game_copy,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
                max_player=True,
            )  # Rozpatrzenie stanu gry po wykonanym ruchu
            # Czy jest to do tej pory stan gry dla przeciwnika
            if rating < min_rating:
                min_rating = rating
                best_move = move
            beta = min(beta, rating)  # Podmiana bety gdy większa niż dotychczas
            # Cięcie alfa-beta
            if beta <= alpha:
                break
        return (
            min_rating,
            best_move,
        )  # Zwraca najmniejszą ocenę i najlepszy ruch przeciwnika


def test_approximate_size_of_decision_tree(
    game: Game,
    alpha: int,
    beta: int,
    max_player: bool,
    curr_depth: int,
    tst: Tree_size_test,
) -> int:
    tst.call_counter += 1
    tst.max_depth = max(tst.max_depth, curr_depth)

    if game.is_end_game:
        return game.get_player_rating(game.curr_player)

    possible_moves = game.all_possible_moves()
    tst.tree_range.append(len(possible_moves))

    if max_player:
        max_rating = Infinity.minus

        for move in possible_moves:
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])
            rating = test_approximate_size_of_decision_tree(
                game=game_copy,
                alpha=alpha,
                beta=beta,
                max_player=False,
                curr_depth=curr_depth + 1,
                tst=tst,
            )
            if tst.call_counter > tst.call_limit:
                break
            if rating > max_rating:
                max_rating = rating
            alpha = max(alpha, rating)
            if beta <= alpha:
                break
        return max_rating
    else:
        min_rating = Infinity.plus

        for move in possible_moves:
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])
            rating = test_approximate_size_of_decision_tree(
                game=game_copy,
                alpha=alpha,
                beta=beta,
                max_player=True,
                curr_depth=curr_depth + 1,
                tst=tst,
            )
            if tst.call_counter > tst.call_limit:
                break
            if rating < min_rating:
                min_rating = rating
            beta = min(beta, rating)
            if beta <= alpha:
                break
        return min_rating


# Funkcja znajdująca najlepszy ruch dla aktualnego stanu planszy,
# Rozpatrując tylko ocenę dla jednego ruchu w przód
def suboptimal_move(game: Game) -> (Vector2, Vector2):
    best_move = None
    max_rating = Infinity.minus

    for move in game.all_possible_moves():
        game_copy = game.deep_copy()
        game_copy.play_turn(move[1], move[0])
        curr_rating = game_copy.get_player_rating(game.curr_player)
        if curr_rating > max_rating:
            max_rating = curr_rating
            best_move = move

    return best_move


# Funkcja zwracająca pseudolosowo wybrany ruch z mozliwych do wykonania
def random_move(game: Game) -> (Vector2, Vector2):
    moves = game.all_possible_moves()

    if moves:
        move = random.choice(moves)
        return move


# EOF
