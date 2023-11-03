from constants import Player, Vector2


class Game:
    board_size: int = None
    board: list[list[Player]] = None
    curr_player: Player = None
    who_won: Player = None
    is_end_game: bool = None

    def __init__(self, size: int = 8) -> None:
        self.board_size = size
        self.__fill_board()
        self.curr_player = Player.White
        self.who_won = Player.Empty
        self.is_end_game = False

    def __fill_board(self) -> None:
        self.board = []

        middle = round(self.board_size / 2)
        empty_rows = [middle, middle - 1]
        if self.board_size % 2 != 0:
            empty_rows.append(middle + 1)

        for x in range(self.board_size):
            row = []
            for y in range(self.board_size):
                if (x + y) % 2 == 0 and not any(x in empty_rows for k in empty_rows):
                    if x < self.board_size / 2:
                        row.append(Player.White)
                    else:
                        row.append(Player.Red)
                else:
                    row.append(Player.Empty)
            self.board.append(row)

    def __move_checker(self, old_pos: Vector2, new_pos: Vector2) -> None:
        self.board[old_pos.x][old_pos.y] = Player.Empty
        self.board[new_pos.x][new_pos.y] = self.curr_player

    def __update_who_won(self) -> None:
        any_white_checker = False
        any_red_checker = False

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == Player.White:
                    any_white_checker = True
                elif self.board[x][y] == Player.Red:
                    any_red_checker = True

                if any_white_checker and any_red_checker:
                    return

        self.who_won = Player.White if any_white_checker == True else Player.Red
        self.is_end_game = True

    def __change_turn(self) -> None:
        self.curr_player = (
            Player.Red if self.curr_player == Player.White else Player.White
        )

    def play_turn(self, old_pos: Vector2, new_pos: Vector2) -> None:
        self.__move_checker(old_pos, new_pos)
        self.__update_who_won()
        if not self.is_end_game:
            self.__change_turn()
