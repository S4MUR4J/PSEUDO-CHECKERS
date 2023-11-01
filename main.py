import os
import math
import time
import random
from array import *

# ? ' ' - empty
# ? 'R' - Red
# ? 'W' - White

n = 6


def init_simulation():
    map = []

    middle = round(n / 2)
    empty_rows = [middle, middle - 1]
    if n % 2 != 0:
        empty_rows.append(middle + 1)

    for i in range(n):
        row = []
        for j in range(n):
            if (i + j) % 2 == 0 and not any(i in empty_rows for k in empty_rows):
                if i < n / 2:
                    row.append("W")
                else:
                    row.append("R")
            else:
                row.append(" ")
        map.append(row)
    return map


def draw_visualization(map):
    os.system("cls")
    i = 0
    j = 0

    while i < len(map):
        if i == 0:
            k = 0
            while k < n:
                print(f" {chr(65 + k)}", end="")
                k += 1
            print("\n")
        while j < len(map):
            print("|" + str(map[i][j]), end="")
            j += 1
            if j == len(map):
                print(f"|  {len(map) - i}")
        j = 0
        i += 1
    print("")


def checkers_able_move(player_turn, map):
    checker = "W" if player_turn == True else "R"
    checker_can_move = []

    for i in range(n):
        for j in range(n):
            if map[i][j] == checker and len(can_move(i, j, map)) > 0:
                checker_can_move.append([i, j])
                print(checker_can_move)

    return checker_can_move


def can_move(x, y, map) -> list:
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


def validate_indexes(index):
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
    white_turn = True
    map = init_simulation()

    while True:
        draw_visualization(map)
        move(checkers_able_move(white_turn, map), map, white_turn)
        
        white_turn = not white_turn
        next_step = input()
        if next_step.lower() == "q":
            break


if __name__ == "__main__":
    main()
