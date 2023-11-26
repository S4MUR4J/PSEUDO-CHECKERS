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

from constants import EnemyMode, Infinity, Player, Vector2, sleep_time
from game import Game
from input import *
from method import *


# Funkcja wizualizująca akualny stan planszy w konsoli
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


# Funkcja przygotowująca, drukująca i zapisująca raport do pliku w folderze projektu
def __print_save_raport(
    board_size: int,
    white_score: int,
    red_score: int,
    move_history: list[str],
    tour_count: int,
    tst: Tree_size_test,
    depth: int,
) -> None:
    # Przygotowanie nazwy pliku na podstawie aktualnej daty i godziny
    file_name = f"MINI_MAX_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"

    # Przygotowanie danych i struktury raportu
    raport = [
        "-------------------------------------------------------------\n",
        f"Raport badania rozmiaru drzewa mini-max w grze w warcaby: \n\n",
        f"Srednia rozpietosc drzewa: {round(sum(tst.tree_range) / len(tst.tree_range), 2)}\n"
        f"Najglebiej polozony wezel: {tst.max_depth} \n"
        f"Oszacowany rozmiar drzewa mini-maks na podstawie limitu {tst.call_limit} wywolan: {tst.tree_size}\n"
        f"-------------------------------------------------------------\n"
        f"Raport algorytmu mini-max w grze w warcaby dla głębokości: {depth}: \n\n",
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


# Funkcja zatrzymująca program na końcu symulacji,
# wywołuje generowanie raportu i zakończa program po wciśnięciu Enter
def __end_simulation(game: Game, tst: Tree_size_test, tree_depth: int) -> None:
    __print_save_raport(
        board_size=game.board_size,
        white_score=game.white_score,
        red_score=game.red_score,
        move_history=game.move_history,
        tour_count=game.tour_count,
        tst=tst,
        depth=tree_depth,
    )
    input("Wciśnij Enter by zakończyć program...")
    os.system("cls")


# Oblicza oszacowaną wartość rozmiaru drzewa mini-maks przy limicie wywołań rekursywnych
def __estimate_tree_size(game: Game, tst: Tree_size_test) -> None:
    os.system("cls")
    print("Trwa szacowanie rozmiaru drzewa mini-max...")
    game_copy = game.deep_copy()
    test_approximate_size_of_decision_tree(
        game=game_copy,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        max_player=game.curr_player,
        curr_depth=1,
        tst=tst,
    )
    tst.tree_size = int(
        (sum(tst.tree_range) / len(tst.tree_range)) ** (tst.max_depth / 2)
    )  # Na podstawie wzoru b^(d/2) dla najlepszego przeszukiwania
    tst.tree_size_no_prune = int(
        (sum(tst.tree_range) / len(tst.tree_range)) ** (tst.max_depth)
    )
    os.system("cls")


# Funkcja odpowiadająca za wywołanie potrzebnych,
# funkcji w celu wizualizacji aktualnej tury
def __visualization(board: list[list[Player]], board_size: int, move: str) -> None:
    os.system("cls")
    __draw_checkboard(board, board_size)
    print(move)
    sleep(sleep_time)


# Funkcja zwracająca parametry symulacji na podstawie decyzji uzytkownika
def __get_game_parameters() -> int | int | int | bool:
    checkboard_size = get_int_input("Prosze o podanie rozmiaru szachownicy: ")
    tree_depth = get_int_input(
        "Prosze o podanie maksymalnej glebokosci drzewa mini-max: "
    )
    enemy_mode = get_int_to_mode_input()
    with_visual = get_yes_no_input("Czy wykonać program z wizualizacją [T/N]: ")
    return checkboard_size, tree_depth, enemy_mode, with_visual


# Funkcja zwracająca najlepszy ruch wyznaczony przy uzyciu algorytmu minimax
def __minimax_move(game: Game, tree_depth: int) -> (Vector2, Vector2):
    _, move = minimax_algorithm(
        game=game,
        depth=tree_depth,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        max_player=game.curr_player,
    )
    return move


# Funkcja dobierająca odpowiednia metode wyznaczenia ruchu na podstawie
# tego, ktorego gracza jest tura i parametrów symulacji
def __move_decider(game: Game, enemy_mode: EnemyMode, tree_depth) -> (Vector2, Vector2):
    if game.curr_player == Player.White:
        return __minimax_move(game, tree_depth)
    else:
        if enemy_mode == EnemyMode.random:
            return random_move(game)

        elif enemy_mode == EnemyMode.suboptimal:
            return suboptimal_move(game.deep_copy())
        else:
            return __minimax_move(game, tree_depth)


def main() -> None:
    sys.setrecursionlimit(100000)
    (
        board_size,
        tree_depth,
        enemy_mode,
        with_visual,
    ) = __get_game_parameters()  # Wczytanie potrzebnych parametrów

    game = Game(board_size)  # Stworzenie instancji gry

    # Oszaczowanie rozmaru drzewa przy maksymalnym milionie wywołań rekursji
    tst = Tree_size_test()
    __estimate_tree_size(game, tst)

    # Pętla symulacji kończy się wraz z zakończeniem gry
    while True:
        # Wykonanie wizualizacji zgodnie z parametrem
        if with_visual:
            __visualization(
                board=game.board, board_size=board_size, move=game.move_history[-1]
            )
        # Koniec gry wyjscie z petli
        if game.is_end_game:
            break

        # Ruch wybierany na podstawie parametrów i aktualnego gracza
        move = __move_decider(game, enemy_mode, tree_depth)
        game.play_turn(move[1], move[0])

    # Zakończenie programu poprzez generowanie raportu oraz informacje
    __end_simulation(game, tst, tree_depth)


if __name__ == "__main__":
    main()

# EOF
