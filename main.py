import os
import math
import time
import random
from array import *

from game import Game
from ui import UI

# ? ' ' - empty
# ? 'R' - Red
# ? 'W' - White

n = 6

def checkers_able_move(player_turn: bool, map: list[list[chr]]) -> list[list[int]]:
    checker = "W" if player_turn == True else "R"
    checker_can_move = []

    for i in range(n):
        for j in range(n):
            if map[i][j] == checker and len(can_move(i, j, map)) > 0:
                checker_can_move.append([i, j])

    print(checker_can_move)
    return checker_can_move


def can_move(x : int, y: int, map: list[list[chr]]) -> list[list[int]]:
    NE = [x + 1, y + 1]
    NW = [x + 1, y - 1]
    SE = [x - 1, y + 1]
    SW = [x - 1, y - 1]
    all_moves = [NE, NW, SE, SW]

    able_moves = []
    for dir in all_moves:
        if not validate_indexes(dir[0]) or not validate_indexes(dir[1]):
            continue
        if map[dir[0]][dir[1]] == " ":
            able_moves.append(dir)

    return able_moves


def validate_indexes(index: int) -> bool:
    return 0 <= index < n - 1
    
def move(checkers: list, map, white_turn) -> None:
    if (len(checkers) == 0):
        print('No moves!!!!')
        return

    choose = random.randrange(0, len(checkers))
    checker = checkers[choose]
    moves = can_move(checker[0], checker[1], map)
    choose2 = random.randrange(0, len(moves))
    move = moves[choose2]

    map[checker[0]][checker[1]] = ' '
    map[move[0]][move[1]] = 'W' if white_turn else 'R'



def main():
    ui = UI()
    game = Game(n)

    while True:
        ui.draw_checkboard(game.checkboard, game.checkboard_size) 
        move(checkers_able_move(game.white_turn, game.checkboard), game.checkboard, game.white_turn)
        
        game.change_turn()
        next_step = input()
        if next_step.upper() == 'Q':
            break


if __name__ == "__main__":
    main()
