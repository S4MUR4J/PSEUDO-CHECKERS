import os
import math
import time
from array import *

# ? 0 - empty
# ? 1 - Red
# ? 2 - White

map = [
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
    ]

def draw_map():
    os.system("cls")
    for i in map:
        for j in i:
            print("|" + str(j), end="")
        print("|")


def main():
    while True:
        draw_map()
        next_step = input()
        if next_step == "Q" or next_step == "q":
            break


if __name__ == "__main__":
    main()
