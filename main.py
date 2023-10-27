import os
import math
import time
from array import *

# ? ' ' - empty
# ? 'R' - Red
# ? 'W' - White

map = [
        [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'],
        ['W', ' ', 'W', ' ', 'W', ' ', 'W', ' '],
        [' ', 'W', ' ', 'W', ' ', 'W', ' ', 'W'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['R', ' ', 'R', ' ', 'R', ' ', 'R', ' '],
        [' ', 'R', ' ', 'R', ' ', 'R', ' ', 'R'],
        ['R', ' ', 'R', ' ', 'R', ' ', 'R', ' '],
    ]

def draw_map():
    os.system("cls")
    i = 0
    j = 0

    while i < len(map):
        if i == 0:
            print('    A B C D E F G H \n')
        while j < len(map):
            if j == 0:
                print(f"{len(map) - i}  ", end="")
            print("|" + str(map[i][j]), end="")
            j += 1
            if j == len(map):
                print(f"|  {len(map) - i}")
        j = 0
        i += 1
        if i == len(map):
            print('\n    A B C D E F G H')


def main():
    while True:
        draw_map()
        next_step = input()
        if next_step == "Q" or next_step == "q":
            break


if __name__ == "__main__":
    main()
