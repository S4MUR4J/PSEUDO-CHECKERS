import os
import math
import time
from array import *

# ? ' ' - empty
# ? 'R' - Red
# ? 'W' - White

n = 8 

def init_simulation():
    map = []

    middle = round(n/2)
    empty_rows = [middle, middle - 1]
    if (n % 2 != 0):
        empty_rows.append(middle + 1)

    for i in range(n):
        row = []
        for j in range(n):
            if (i + j) % 2 == 0 and not any(i in empty_rows for k in empty_rows):
                if i < n/2:
                    row.append('W')
                else:
                    row.append('R')
            else:
                row.append(' ')
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
                print(f' {chr(65 + k)}', end='')
                k += 1
            print('\n')
        while j < len(map):
            print("|" + str(map[i][j]), end='')
            j += 1
            if j == len(map):
                print(f"|  {len(map) - i}")
        j = 0
        i += 1


def main():
    map = init_simulation()

    while True:
        draw_visualization(map)

        next_step = input()
        if next_step == "Q" or next_step == "q":
            break


if __name__ == "__main__":
    main()
