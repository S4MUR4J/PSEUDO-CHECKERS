# Author: Maciej Mucha

# method.py Realizacja zadanej metody sztucznej inteligencji mini-max
# oraz funkcji znajdowania suboptymalnego i losowego ruchu

import random

from constants import Infinity, Player, Vector2
from game import Game


def minimax_algorithm(
    game: Game, depth: int, alpha: int, beta: int, max_player: Player
) -> int | Vector2:
    best_move = None

    # Sprawdzenie czy jesteśmy na ostatnim poziomie drzewa mini-maks
    if depth == 0 or game.is_end_game:
        return (
            game.get_player_rating(max_player),
            best_move,
        )  # Ocena stanu gry dla gracza maksymalizującego, bez najlepszego ruchu

    # Kopia stanu gry przed sprawdzaniem
    # będzie przypisywana do game_inner w celu oszczędzenia zasobów
    game_copy = game.deep_copy()

    # Sprawdzanie na gracza maksymalizującego
    if game.curr_player == Player:
        max_rating = (
            Infinity.minus
        )  # Dla początku rozpatrywania drzewa nieosiągalna wartość

        # Rozpatrywanie każdego możliwego ruchu z danego stanu gry
        for move in game.all_possible_moves():
            game_inner = game_copy
            game_inner.play_turn(move[1], move[0])  # Wykonanie ruchu na kopii
            rating, _ = minimax_algorithm(
                game=game_inner,
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
            game_inner = game_copy
            game_inner.play_turn(move[1], move[0])  # Wykonanie ruchu na kopii
            rating, _ = minimax_algorithm(
                game=game_inner,
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


# Funkcja znajdująca najlepszy ruch dla aktualnego stanu planszy,
# Rozpatrując tylko ocenę dla jednego ruchu w przód
def suboptimal_move(game: Game) -> (Vector2, Vector2):
    best_move = None
    max_rating = Infinity.minus

    for move in game.all_possible_moves():
        game_inner = game
        game_inner.play_turn(move[1], move[0])
        curr_rating = game_inner.get_player_rating()
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
