import os
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
        self, board: list[list[chr]], board_size: int, who_won: Player
    ) -> None:
        os.system("cls")
        self.__draw_checkboard(board, board_size)
        self.__draw_heuristics(board, board_size)
        sleep(self.__sleep_time)
        if who_won != Player.White:
            print(f'{'Biały' if who_won == Player.White else 'Czerwony'} wygrał grę \n')

    def generate_raport(self) -> None:
        # TODO Generowanie raportu
        print("Raport został wygenerowany na pulpicie B)... \n")

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

    def __draw_checkboard(
        self, checkboard: list[list[chr]], checkboard_size: int
    ) -> None:
        for x in range(checkboard_size):
            if x == 0:
                for i in range(checkboard_size):
                    print(f" {chr(65 + i)}", end="")
                print("\n")
            for y in range(checkboard_size):
                print(f"|{str(checkboard[x][y])}", end="")
                if y == checkboard_size - 1:
                    print(f"|  {checkboard_size - x}")
        print("")

    def __draw_heuristics(
        self, checkboard: list[list[chr]], checkboard_size: int
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
