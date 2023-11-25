# Author: Maciej Mucha

###########################################################

# O programie

# Program realizujący zadanie symulacji gry dwóch graczy w grze w warcaby
# Komputer steruje warcabami z czego Biały wybiera ruchy na podstawie algorytmu mini-max
# Wybór ruchów gracza czerwonego odbywa się na podstawie wyboru użytkownika
# Użytkownik ma możliwość wpisania wybranych przez niego parametrów symulacji

###########################################################

# main.py - Realizacja sterowania nad symulacją

import math
import sys
from datetime import datetime
from time import sleep

from constants import EnemyMode, Infinity, Player, Vector2
from game import Game
from input import *
from method import *


# Funkcja rysująca akualny stan planszy w konsoli
def __draw_checkboard(board: list[list[Player]], board_size: int) -> None:
    for x in range(board_size):
        if x == 0:
            for i in range(board_size):
                print(
                    f" {chr(65 + i)}", end=""
                )  # Drukowanie nazwy konkretnej pozycji na osi X (A, B, C...)
            print("\n")
        for y in range(board_size):
            print(
                f"|{board[board_size - x - 1][board_size - y - 1].value}", end=""
            )  # Drukowanie zawartości konkretnej pozycji warcabnicy
            if y == board_size - 1:
                print(
                    f"|  {board_size - x}"
                )  # Drukowanie nazwy konkretnej pozycji na osi Y (1, 2, 3...)
    print("")


# Funkcja zatrzymująca program na końcu symulacji,
# zakończenie programu po wciśnięciu Enter
def end_simulation(
    board_size: int,
    white_score: int,
    red_score: int,
    move_history: list[str],
    tour_count: int,
) -> None:
    __print_save_raport(
        board_size=board_size,
        white_score=white_score,
        red_score=red_score,
        move_history=move_history,
        tour_count=tour_count,
    )
    input("Wciśnij Enter by zakończyć program...")
    os.system("cls")


# Funkcja odpowiadająca za wywołanie potrzebnych,
# funkcji w celu wizualizacji aktualnej tury
def visualization(board: list[list[Player]], board_size: int, move: str) -> None:
    os.system("cls")
    __draw_checkboard(board, board_size)
    print(move)
    sleep(1)


# Funkcja przygotowująca i zapisująca raport do pliku w folderze projektu
def __print_save_raport(
    board_size: int,
    white_score: int,
    red_score: int,
    move_history: list[str],
    tour_count: int,
) -> None:
    # Przygotowanie nazwy pliku na podstawie aktualnej daty i godziny
    file_name = f"MINI_MAX_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"

    # Przygotowanie danych i struktury raportu
    raport = [
        "-------------------------------------------------------------\n",
        "Raport algorytmu mini-max w grze w warcaby: \n\n",
        f"Gra wykonana na warcabnicy: {board_size} x {board_size}. \n",
        f'Rozgrywke wygral: {"Bialy" if white_score > red_score else "Czerwony"}. \n',
        f"Gracz Bialy wykonal ruchow: {math.ceil(tour_count / 2)}\n",
        f"Gracz Czerwony wykonal ruchow: {math.floor(tour_count / 2)}\n",
        f"Liczba punktow gracza bialego: {white_score} \n",
        f"Liczba punktow gracza czerwonego: {red_score} \n",
        "-------------------------------------------------------------",
    ]

    # Drukowanie podsumowania w konsoli
    for data in raport:
        print(data)

    # Rozszerzenie o historię ruchów
    raport.append(f"\nHistoria ruchow: \n")
    for move in move_history:
        raport.append(move)

    # Zapis do pliku
    file = open(file_name, "w")

    for data in raport:
        file.writelines(data)
    file.close()

    # Powiadomienie o wygenerowanym pliku
    print(f"W folderze projektu został wygenerowany raport: {file_name}... \n")


# Funkcja zwracająca parametry symulacji na podstawie decyzji uzytkownika
def __get_game_parameters() -> int | int | int | int | bool | float:
    checkboard_size = get_int_input("Prosze o podanie rozmiaru szachownicy: ")
    enemy_mode = get_int_to_mode_input()
    with_visual = get_yes_no_input("Czy wykonać program z wizualizacją [T/N]: ")
    return checkboard_size, enemy_mode, with_visual


# Funkcja zwracająca najlepszy ruch wyznaczony przy uzyciu algorytmu minimax
def __minimax_move(game: Game) -> (Vector2, Vector2):
    game_copy = game.deep_copy()
    _, move = minimax_algorithm(
        game=game_copy,
        depth=100000,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        max_player=game.curr_player,
    )
    return move


# Funkcja dobierająca odpowiednia metode wyznaczenia ruchu na podstawie
# tego, ktorego gracza jest tura i parametrów symulacji
def __move_decider(game: Game, enemy_mode: EnemyMode) -> (Vector2, Vector2):
    if game.curr_player == Player.White:
        return __minimax_move(game)
    else:
        if enemy_mode == EnemyMode.random:
            return random_move(game)

        elif enemy_mode == EnemyMode.suboptimal:
            return suboptimal_move(game.deep_copy())
        else:
            return __minimax_move(game)


def main() -> None:
    sys.setrecursionlimit(1000000)
    (
        board_size,
        enemy_mode,
        with_visual,
    ) = __get_game_parameters()  # Wczytanie potrzebnych parametrów

    game = Game(board_size)  # Stworzenie instancji gry

    # Pętla symulacji kończy się wraz z zakończeniem gry
    while True:
        # Wykonanie wizualizacji zgodnie z parametrem
        if with_visual:
            visualization(
                board=game.board, board_size=board_size, move=game.move_history[-1]
            )
        # Koniec gry wyjscie z petli
        if game.is_end_game:
            break

        # Ruch wybierany na podstawie parametrów i aktualnego gracza
        move = __move_decider(game, enemy_mode)
        if move:
            game.play_turn(move[1], move[0])

    # Zakończenie programu poprzez generowanie raportu oraz informacje
    end_simulation(
        board_size=board_size,
        white_score=game.white_score,
        red_score=game.red_score,
        move_history=game.move_history,
        tour_count=game.tour_count,
    )


if __name__ == "__main__":
    main()

# EOF
