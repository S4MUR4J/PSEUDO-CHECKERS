# ui.py | Author : Maciej Mucha

import os
from datetime import datetime
from time import sleep

from constants import EnemyMode, Mode, Player


def __clear_screen() -> None:
    os.system("cls")


def __wrong_input() -> None:
    input("Nieprawidłowy decyzja, naciśnij klawisz by powtórzyć...")


def __draw_checkboard(board: list[list[Player]], board_size: int) -> None:
    for x in range(board_size):
        if x == 0:
            for i in range(board_size):
                print(f" {chr(65 + i)}", end="")
            print("\n")
        for y in range(board_size):
            print(f"|{board[board_size - x - 1][board_size - y - 1].value}", end="")
            if y == board_size - 1:
                print(f"|  {board_size - x}")
    print("")


def get_int_input(message: str) -> int:
    while True:
        __clear_screen()
        try:
            value = int(input(message))
        except ValueError:
            __wrong_input()
        else:
            return value


def get_float_input(message: str) -> float:
    while True:
        __clear_screen()
        try:
            time = float(input(message))
        except ValueError:
            __wrong_input()
        else:
            return time


def get_yes_no_input(message: str) -> bool:
    choice = ""
    while True:
        __clear_screen()
        choice = str(input(message))
        if choice.upper() == str("T"):
            return True
        if choice.upper() == str("N"):
            return False
        __wrong_input()


def get_int_to_mode_input() -> Mode:
    while True:
        __clear_screen()
        print("Tryby gry przeciwnika")
        print("1. Losowy")
        print("2. Suboptymalny")
        print("3. Minimax")

        try:
            value = int(input("Proszę o wybranie trybu przeciwnika [1-3]: "))
        except ValueError:
            __wrong_input()
        else:
            if value > 0 and value <= 3:
                if value == 1:
                    return EnemyMode.random
                elif value == 2:
                    return EnemyMode.suboptimal
                else:
                    return EnemyMode.minimax

            __wrong_input()


def end_simulation() -> None:
    print("\n")
    input("Wciśnij Enter by zakończyć program...")
    __clear_screen()


# TODO Game class based
def __write_move(move: str) -> None:
    print(move)


def visualization(
    board: list[list[Player]], board_size: int, sleep_time: float
) -> None:
    __clear_screen()
    __draw_checkboard(board, board_size)
    sleep(sleep_time)


# TODO Game class based
def generate_raport(
    board_size: int,
    who_won: Player,
    white_score: int,
    red_score: int,
    tour_count: int,
) -> None:
    file_name = f"MINI_MAX_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"

    raport = [
        "Raport algorytmu mini-max w grze w warcaby: \n\n",
        f"Gra wykonana na warcabnicy: {board_size} x {board_size}. \n",
        f'Rozgrywke wygral: {"Biały" if who_won == Player.White else "Czerwony"}. \n',
        f"Liczba punktow gracza bialego: {white_score} \n"
        f"Liczba punktow gracza czerwonego: {red_score} \n"
        f"Gra trwala {tour_count} tur. \n"
        # TODO Kolejność ruchów
        # TODO dodatkowe
    ]

    file = open(file_name, "w")

    for data in raport:
        file.writelines(data)
    file.close()

    print(f"W folderze projektu został wygenerowany raport: {file_name}... \n")


# EOF
