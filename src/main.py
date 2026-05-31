import math
import os
import sys
from datetime import datetime
from time import sleep

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import *
from src.game import Game
from src.input import *
from src.method import *


def __draw_checkboard(board: list[list[Player]], board_size: int) -> None:
    for x in range(board_size):
        if x == 0:
            for i in range(board_size):
                print(f" {chr(65 + i)}", end="")  # X-axis: A, B, C...
            print("\n")
        for y in range(board_size):
            print(f"|{board[board_size - x - 1][board_size - y - 1].value}", end="")
            if y == board_size - 1:
                print(f"|  {board_size - x}")  # Y-axis: 1, 2, 3...
    print("")


def __print_save_raport(
    board_size: int,
    white_score: int,
    red_score: int,
    move_history: list[str],
    tour_count: int,
    tst: Tree_size_test,
    depth: int,
    enemy_mode: EnemyMode,
) -> None:
    file_name = f"MINI_MAX_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"

    raport = [
        "-------------------------------------------------------------\n",
        f"Report on minimax decision tree size analysis in checkers: \n\n",
        f"Average tree branching factor: {round(sum(tst.tree_range) / len(tst.tree_range), 2)}\n"
        f"Deepest node: {tst.max_depth} \n"
        f"Estimated minimax tree size based on limit of {tst.call_limit} recursive calls: {tst.tree_size}\n\n"
        f"-------------------------------------------------------------\n\n"
        f"Minimax algorithm report in checkers for depth {depth}: \n\n",
        f"Opponent mode: {enemy_mode.value} \n\n"
        f"Game played on board: {board_size} x {board_size}. \n",
        f'Winner: {"White" if white_score > red_score else "Red"}. \n',
        f"White player moves: {math.ceil(tour_count / 2)}\n",
        f"Red player moves: {math.floor(tour_count / 2)}\n",
        f"White player score: {white_score} \n",
        f"Red player score: {red_score} \n",
        "-------------------------------------------------------------",
    ]

    for data in raport:
        print(data)

    raport.append(f"\nMove history: \n")
    for move in move_history:
        raport.append(move)

    file = open(file_name, "w")
    for data in raport:
        file.writelines(data)
    file.close()

    print(f"Report generated in project folder: {file_name}... \n")


def __end_simulation(
    game: Game, tst: Tree_size_test, tree_depth: int, enemy_mode: EnemyMode
) -> None:
    __print_save_raport(
        board_size=game.board_size,
        white_score=game.white_score,
        red_score=game.red_score,
        move_history=game.move_history,
        tour_count=game.tour_count,
        tst=tst,
        depth=tree_depth,
        enemy_mode=enemy_mode,
    )
    input("Press Enter to exit...")
    os.system("cls")


def __estimate_tree_size(game: Game, tst: Tree_size_test) -> None:
    os.system("cls")
    print("Estimating minimax tree size...")
    game_copy = game.deep_copy()
    test_aproximate_size_of_decision_tree(
        game=game_copy,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        max_player=game.curr_player,
        curr_depth=1,
        tst=tst,
    )
    tst.tree_size = int(
        math.ceil(sum(tst.tree_range) / len(tst.tree_range)) ** (tst.max_depth / 2)
    )  # Formula b^(d/2) for alpha-beta with optimal move ordering
    input(
        f"Maximum tree depth for this board is {tst.max_depth}, press Enter to continue."
    )


def __visualization(board: list[list[Player]], board_size: int, move: str) -> None:
    os.system("cls")
    __draw_checkboard(board, board_size)
    print(move)
    sleep(sleep_time)


def __get_game_parameters() -> tuple[int, int, EnemyMode, bool, Tree_size_test]:
    checkboard_size = get_int_input("Please enter the board size: ", 3)

    tst = Tree_size_test()
    __estimate_tree_size(Game(checkboard_size), tst)
    tree_depth = get_int_input(
        "Please enter the maximum minimax tree depth: ", 1
    )

    enemy_mode = get_int_to_mode_input()
    with_visual = get_yes_no_input("Run program with visualization [Y/N]: ")
    return checkboard_size, tree_depth, enemy_mode, with_visual, tst


def __minimax_move(game: Game, tree_depth: int) -> tuple[Vector2, Vector2]:
    _, move = minimax_algorithm(
        game=game,
        depth=tree_depth,
        alpha=Infinity.minus,
        beta=Infinity.plus,
        max_player=game.curr_player,
    )
    return move


def __move_decider(game: Game, enemy_mode: EnemyMode, tree_depth) -> tuple[Vector2, Vector2]:
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
    sys.setrecursionlimit(recursion_limit)
    (
        board_size,
        tree_depth,
        enemy_mode,
        with_visual,
        tst,
    ) = __get_game_parameters()

    game = Game(board_size)

    while True:
        if with_visual:
            __visualization(
                board=game.board, board_size=board_size, move=game.move_history[-1]
            )
        if game.is_end_game:
            break

        move = __move_decider(game.deep_copy(), enemy_mode, tree_depth)
        game.play_turn(move[1], move[0], True)

    __end_simulation(game, tst, tree_depth, enemy_mode)


if __name__ == "__main__":
    main()
