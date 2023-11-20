import os
from datetime import datetime
from time import sleep

from constants import EnemyMode, Mode, Player


class Control:
    min_max_depth: int = None
    checkboard_size: int = None
    enemy_mode: EnemyMode = None
    with_visualization: bool = None
    __sleep_time: float = None

    def __init__(self) -> None:
        self.min_max_depth = self.__get_int_input(
            "Prosze o podanie maksymalnej liczby ruchów jednego gracza"
        )
        self.checkboard_size = self.__get_int_input(
            "Prosze o podanie rozmiaru szachownicy: "
        )
        self.with_visualization = self.__get_yes_no_input(
            "Czy wykonać program z wizualizacją [T/N]: "
        )
        self.__sleep_time = self.__get_float_input(
            "Prosze o podanie czasu oczekiwania na kolejny ruch: "
        )

    def visualization(
        self,
        board: list[list[Player]],
        board_size: int,
    ) -> None:
        os.system("cls")
        self.__draw_checkboard(board, board_size)
        sleep(self.__sleep_time)

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

    def generate_raport(
        self,
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

    def end_simulation(self) -> None:
        input("Wciśnij Enter by zakończyć program...")

    # ! Nie przygotowane
    def __write_move(self, move: str) -> None:
        print(move)

    def __get_int_input(self, message: str) -> int:
        while True:
            try:
                value = int(input(message))
            except ValueError:
                self.__wrong_input()
            else:
                return value

    def __get_float_input(self, message: str) -> float:
        if self.with_visualization is False:
            return 0
        while True:
            try:
                time = float(input(message))
            except ValueError:
                self.__wrong_input()
            else:
                return time

    # TODO
    def __get_int_to_mode_input() -> Mode:
        return EnemyMode.minimax

    def __get_yes_no_input(self, message: str) -> bool:
        choice = ""
        while self.with_visualization == None:
            choice = str(input(message))
            if choice.upper() == str("T"):
                return True
            if choice.upper() == str("N"):
                return False
            self.__wrong_input()

    def __wrong_input(self) -> None:
        input("Nieprawidłowy decyzja, naciśnij klawisz by powtórzyć...")
