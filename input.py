# Author : Maciej Mucha

# input.py - Plik przechowujący funkcje odpowiadające za odczyt danych wejściowych użytkownika i ich walidację

import os

from constants import EnemyMode


# Funkcja informująca o niepoprawnie wprowadzonej informacji
def __wrong_input() -> None:
    input("Nieprawidłowa decyzja, naciśnij klawisz by powtórzyć...")


# Funkcja czytająca i walidująca dane wejściowe typu int
def get_int_input(message: str) -> int:
    while True:
        os.system("cls")
        try:
            value = int(input(message))
        except ValueError:
            __wrong_input()
        else:
            return value


# Funkcja czytająca i walidująca dane wejściowe wybóru TAK/NIE
def get_yes_no_input(message: str) -> bool:
    choice = ""
    while True:
        os.system("cls")
        choice = str(input(message))
        if choice.upper() == str("T"):
            return True
        if choice.upper() == str("N"):
            return False
        __wrong_input()


# Funkcja czytająca i walidująca dane wejściowe wybóru trybu gry przeciwnika
def get_int_to_mode_input() -> EnemyMode:
    while True:
        os.system("cls")
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


# EOF
