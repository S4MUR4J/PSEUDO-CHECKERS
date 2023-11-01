import os
import random
from array import *
from types import NoneType
from checkboard import Checkboard
from constants import Turn, Vector2
from game import Game

from ui import UI
n = 6


def checkers_able_move(checkers: chr, map: list[list[chr]]) -> list[list[int]]:
    checker = checkers
    checker_can_move = []

    for i in range(n):
        for j in range(n):
            if map[i][j] == checker and len(can_move(i, j, map)) > 0:
                checker_can_move.append(Vector2(i, j))

    print(checker_can_move)
    return checker_can_move


def can_move(x: int, y: int, map: list[list[chr]]) -> list[Vector2]:
    NE = Vector2(x + 1, y + 1)
    NW = Vector2(x + 1, y - 1)
    SE = Vector2(x - 1, y + 1)
    SW = Vector2(x - 1, y - 1)
    all_moves = [NE, NW, SE, SW]

    able_moves = []
    for dir in all_moves:
        if not validate_indexes(dir.x) or not validate_indexes(dir.y):
            continue
        if map[dir.x][dir.y] == " ":
            able_moves.append(dir)

    return able_moves


def validate_indexes(index: int) -> bool:
    return 0 <= index < n - 1


def move_old(checkers: list[Vector2], map) -> (Vector2, Vector2):
    if len(checkers) == 0:
        print("No moves!!!!")
        return

    choose = random.randrange(0, len(checkers))
    checker = checkers[choose]
    moves = can_move(checker.x, checker.y, map)
    choose2 = random.randrange(0, len(moves))
    move = moves[choose2]

    return checker, move

def main() -> None:
    ui = UI()
    checkboard = Checkboard(n)
    game = Game()

    ui.draw_checkboard(checkboard.board, checkboard.size)

    while True:
        quit = input('Q - wyjście: ')
        if quit.upper() == 'Q':
            break

        os.system('cls')
        game.change_turn()
        result = move_old(
            checkers_able_move(game.get_turn_checker, checkboard.board), checkboard.board
        )

        if type(result) is not NoneType:
            checkboard.move_checker(result[0], result[1], game.get_turn_checker)
        ui.draw_checkboard(checkboard.board, checkboard.size)

if __name__ == "__main__":
    main()
