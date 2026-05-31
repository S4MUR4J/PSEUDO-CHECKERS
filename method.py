import random

from constants import Infinity, Player, Tree_size_test, Vector2
from game import Game


def minimax_algorithm(
    game: Game, depth: int, alpha: int, beta: int, max_player: bool
) -> int | Vector2:
    if depth == 0 or game.is_end_game:
        return game.get_player_rating(game.curr_player), None

    best_move = None

    if max_player:
        max_rating = Infinity.minus

        for move in game.all_possible_moves():
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])
            rating, _ = minimax_algorithm(
                game=game_copy,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
                max_player=False,
            )
            if rating > max_rating:
                max_rating = rating
                best_move = move
            alpha = max(alpha, rating)
            if beta <= alpha:  # Alpha-beta cut
                break
        return max_rating, best_move

    else:
        min_rating = Infinity.plus

        for move in game.all_possible_moves():
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])
            rating, _ = minimax_algorithm(
                game=game_copy,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
                max_player=True,
            )
            if rating < min_rating:
                min_rating = rating
                best_move = move
            beta = min(beta, rating)
            if beta <= alpha:  # Alpha-beta cut
                break
        return min_rating, best_move


def test_aproximate_size_of_decision_tree(
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
    tst.tree_range.append(len(possible_moves))  # Record branching factor at this depth

    if max_player:
        max_rating = Infinity.minus

        for move in possible_moves:
            game_copy = game.deep_copy()
            game_copy.play_turn(move[1], move[0])
            rating = test_aproximate_size_of_decision_tree(
                game=game_copy,
                alpha=alpha,
                beta=beta,
                max_player=False,
                curr_depth=curr_depth + 1,
                tst=tst,
            )
            if tst.call_counter > tst.call_limit:  # Stop analysis after reaching the call limit
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
            rating = test_aproximate_size_of_decision_tree(
                game=game_copy,
                alpha=alpha,
                beta=beta,
                max_player=True,
                curr_depth=curr_depth + 1,
                tst=tst,
            )
            if tst.call_counter > tst.call_limit:  # Stop analysis after reaching the call limit
                break
            if rating < min_rating:
                min_rating = rating
            beta = min(beta, rating)
            if beta <= alpha:
                break
        return min_rating


# Evaluates only one move ahead, hence "suboptimal"
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


def random_move(game: Game) -> (Vector2, Vector2):
    moves = game.all_possible_moves()

    if moves:
        move = random.choice(moves)
        return move
