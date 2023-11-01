import random

from constants import Player, Vector2


class Algorithm:
    def __init__(self) -> None:
        pass

    def find_best_checker(
        self, board: list[list[chr]], board_size: int, player: Player
    ) -> (Vector2, Vector2):
        checkers = []

        for x in range(board_size):
            for y in range(board_size):
                if (
                    board[x][y] == player.value
                    and len(self.__find_best_move(Vector2(x, y), board, board_size)) > 0
                ):
                    checkers.append(Vector2(x, y))

        checker = checkers[random.randrange(0, len(checkers))]
        moves = self.__find_best_move(checker, board, board_size)
        move = moves[random.randrange(0, len(moves))]

        return checker, move

    def __find_best_move(
        self, checker: Vector2, board: list[list[chr]], board_size: int
    ) -> Vector2:
        all_moves = [
            Vector2(checker.x + 1, checker.y + 1),
            Vector2(checker.x + 1, checker.y - 1),
            Vector2(checker.x - 1, checker.y + 1),
            Vector2(checker.x - 1, checker.y - 1),
        ]

        able_moves = []
        for dir in all_moves:
            if not self.__validate_indexes(
                dir.x, board_size
            ) or not self.__validate_indexes(dir.y, board_size):
                continue
            if board[dir.x][dir.y] == Player.Empty.value:
                able_moves.append(dir)

        return able_moves

    def __validate_indexes(self, index: int, board_size: int) -> bool:
        return 0 <= index < board_size - 1
