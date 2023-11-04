import os
from datetime import datetime
from time import sleep

from constants import Player


class UI:
    checkboard_size: int = None
    with_visualization: bool = None
    __sleep_time: float = None

    def __init__(self) -> None:
        self.checkboard_size = self.__read_checkboard_size()
        self.with_visualization = self.__read_visualization_choice()
        self.__sleep_time = self.__read_sleep_time()

    def visualization(
        self,
        board: list[list[Player]],
        board_size: int,
    ) -> None:
        os.system("cls")
        self.__draw_checkboard(board, board_size)
        self.__draw_heuristics(board, board_size)
        sleep(self.__sleep_time)

    def generate_raport(
        self,
        board_size: int,
        who_won: Player,
        white_score: int,
        red_score: int,
        tour_count: int,
    ) -> None:
        file_name = f"MIN_MAX_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"

        raport = [
            "Raport algorytmu mini-max w grze w warcaby: \n\n",
            f"Gra wykonana na szachownicy: {board_size} x {board_size}. \n",
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

    def __read_checkboard_size(self) -> int:
        while True:
            try:
                size = int(input("Prosze o podanie rozmiaru szachownicy: "))
            except ValueError:
                self.__wrong_input()
            else:
                return size

    def __read_visualization_choice(self) -> bool:
        choice = ""
        while self.with_visualization == None:
            choice = str(input("Czy wykonać program z wizualizacją [Y/N]: "))
            if choice.upper() == str("Y"):
                return True
            if choice.upper() == str("N"):
                return False
            input("Nieprawidłowy typ danych, naciśnij klawisz by powtórzyć...")

    def __read_sleep_time(self) -> float:
        if self.with_visualization is False:
            return 0
        while True:
            try:
                time = float(
                    input("Prosze o podanie czasu oczekiwania na kolejny ruch: ")
                )
            except ValueError:
                self.__wrong_input()
            else:
                return time

    def __wrong_input(self) -> None:
        input("Nieprawidłowy typ danych, naciśnij klawisz by powtórzyć...")

    # To moze byc jedna funkcja w przyszłości

    def __write_move(self, move: str) -> None:
        print(move)

    def __draw_checkboard(self, board: list[list[Player]], board_size: int) -> None:
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

    def __draw_heuristics(
        self, board: list[list[Player]], checkboard_size: int
    ) -> None:
        mock = "X"

        for x in range(checkboard_size):
            if x == 0:
                for i in range(checkboard_size):
                    print(f" {chr(65 + i)}", end="")
                print("\n")
            for y in range(checkboard_size):
                print(f"|{mock}", end="")
                if y == checkboard_size - 1:
                    print(f"|  {checkboard_size - x}")
        print("")
