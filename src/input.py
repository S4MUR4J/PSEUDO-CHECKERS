import os

from src.constants import EnemyMode


def __wrong_input() -> None:
    input("Invalid input, press any key to try again...")


def get_int_input(message: str, min: int) -> int:
    while True:
        os.system("cls")
        try:
            value = int(input(message))
        except ValueError:
            __wrong_input()
        else:
            if value >= min:
                return value
            print(f"Value too small, minimum value: {min}")
            __wrong_input()


def get_yes_no_input(message: str) -> bool:
    choice = ""
    while True:
        os.system("cls")
        choice = str(input(message))
        if choice.upper() == str("Y"):
            return True
        if choice.upper() == str("N"):
            return False
        __wrong_input()


def get_int_to_mode_input() -> EnemyMode:
    while True:
        os.system("cls")
        print("Opponent game modes")
        print("1. Random")
        print("2. Suboptimal")
        print("3. Minimax")

        try:
            value = int(input("Please select opponent mode [1-3]: "))
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
