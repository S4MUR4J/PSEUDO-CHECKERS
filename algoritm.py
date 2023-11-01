import random
from constants import Vector2


class Algorithm:

    def __init__(self) -> None:
        pass

    def find_best_checker(self, board : list[list[chr]], board_size : int, player : chr) -> (Vector2, Vector2):
        checkers : Vector2 = []

        for x in range(board_size):
                for y in range(board_size):
                    if board[x][y] == player and len(self.__find_best_move(Vector2(x, y), board, board_size)) > 0:
                        checker.append(Vector2(x, y))

        checker = checkers[random.randrange(0, len(checkers))]
        moves = self.__find_best_move(checker, board, board_size)
        move = moves[random.randrange(0, len(moves))]
        
    def __find_best_move(self, checker : Vector2, board : list[list[chr]], board_size : int) -> Vector2:
        all_moves = [
            Vector2(checker.x + 1, checker.y + 1),
            Vector2(checker.x + 1, checker.y - 1),
            Vector2(checker.x - 1, checker.y + 1),
            Vector2(checker.x - 1, checker.y - 1),
        ]

        able_moves = []
        for dir in all_moves:
                if not self.__validate_indexes(dir.x) or not self.__validate_indexes(dir.y):
                    continue
                if board[dir.x][dir.y] == " ":
                    able_moves.append(dir)

        return able_moves


    def __validate_indexes(index : int, board_size : int) -> bool:
        return 0 <= index < board_size - 1