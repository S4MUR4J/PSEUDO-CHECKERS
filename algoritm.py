from constants import Infinity, Vector2
from game import Game


def minimax_algorithm(
    game: Game, depth: int, alpha: int, beta: int, maximazing: bool
) -> int | Vector2:
    best_move = None

    # Sprawdzenie czy jesteśmy na ostatnim poziomie drzewa mini-maks
    if depth == 0 or game.is_end_game:
        return (
            game.get_rating(),
            best_move,
        )  # Ocena stanu gry na końcu drzewa, bez najlepszego ruchu

    # Kopia stanu gry przed sprawdzaniem
    # będzie przypisywana do game_inner w celu oszczędzenia zasobów
    game_copy = game.deep_copy()

    # Sprawdzanie na gracza maksymalizującego
    if maximazing:
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
                maximazing=False,
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
                maximazing=True,
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
