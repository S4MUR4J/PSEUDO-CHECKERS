from constants import Player, Vector2
from game import Game


class Algorithm:
    max_depth: int = None

    def __init__(self, max_depth=float("inf")):
        self.max_depth = max_depth

    def __get_heuristics(self, game: Game) -> int:
        if game.curr_player == Player.White:
            return game.white_score - game.red_score
        else:
            return game.red_score - game.white_score

    def minimax_algorithm(
        self, game: Game, depth: int, alpha: int, beta: int, max_player: bool
    ):
        best_move = None

        if depth == 0 or game.is_end_game:
            return self.__get_heuristics(game), best_move

        game_copy = game.deep_copy()
        if max_player:
            max_heuristic = float("-inf")
            for move in game.all_possible_moves():
                game_inner = game_copy
                game_inner.play_turn(move[1], move[0])
                heuristic, _ = self.minimax_algorithm(
                    game_inner, depth - 1, alpha, beta, False
                )
                if heuristic > max_heuristic:
                    max_heuristic = heuristic
                    best_move = move
                alpha = max(alpha, heuristic)
                if beta <= alpha:
                    break
            return max_heuristic, best_move
        else:
            min_heuristic = float("inf")
            for move in game.all_possible_moves():
                game_inner = game_copy
                game_inner.play_turn(move[1], move[0])
                heuristic, _ = self.minimax_algorithm(
                    game_inner, depth - 1, alpha, beta, True
                )
                if heuristic < min_heuristic:
                    min_heuristic = heuristic
                    best_move = move
                beta = min(beta, heuristic)
                if beta <= alpha:
                    break
            return min_heuristic, best_move
