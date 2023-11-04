from constants import Directions, Player, Vector2


class Game:
    board_size: int = None
    board: list[list[Player]] = None
    curr_player: Player = None
    who_won: Player = None
    is_end_game: bool = None
    tour_count: int = None
    move_history: list[str] = []

    white_score: int = None
    red_score: int = None

    def __init__(self, size: int = 8) -> None:
        self.board_size = size
        self.__fill_board()
        self.curr_player = Player.White
        self.who_won = Player.Empty
        self.is_end_game = False
        self.white_score = 0
        self.red_score = 0
        self.tour_count = 0
        self.list_string = []

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
        if abs(old_pos.x - new_pos.x) > 1:
            capt_pos = Vector2(
                (old_pos.x + new_pos.x) // 2, (old_pos.y + new_pos.y) // 2
            )
            self.board[capt_pos.x][capt_pos.y] = Player.Empty
            if self.curr_player == Player.White:
                self.white_score += 1
            else:
                self.red_score += 1

        self.board[old_pos.x][old_pos.y] = Player.Empty
        self.board[new_pos.x][new_pos.y] = self.curr_player
        self.move_history.append(
            f"{chr(65 + old_pos.x)}{old_pos.y + 1} -> {chr(65 + new_pos.x)}{new_pos.y + 1} \n"
        )

    def __update_game_end(self) -> None:
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

    def __score_king(self, pos: Vector2) -> None:
        if (self.curr_player == Player.White and pos.x == self.board_size - 1) or (
            self.curr_player == Player.Red and pos.x == 0
        ):
            self.board[pos.x][pos.y] = Player.Empty

            if self.curr_player == Player.White:
                self.white_score += 1
            if self.curr_player == Player.Red:
                self.red_score += 1

    def __validate_indexes(self, new_pos: Vector2) -> bool:
        return 0 <= new_pos.x < self.board_size and 0 <= new_pos.y < self.board_size

    # TODO dodać parametr wywołujący sprawdzanie skoków
    def __possible_moves(self, pos: Vector2) -> list[Vector2]:
        possible_moves = []
        directions = Directions().get()

        if self.board[pos.x][pos.y] == self.curr_player:
            for dir in directions:
                new_pos = Vector2(pos.x + dir.x, pos.y + dir.y)
                if self.__validate_indexes(new_pos):
                    if self.board[new_pos.x][new_pos.y] == Player.Empty and (
                        (self.curr_player == Player.White and dir.x > 0)
                        or (self.curr_player == Player.Red and dir.x < 0)
                    ):
                        possible_moves.append(new_pos)
                    elif self.board[new_pos.x][new_pos.y] == (
                        Player.Red if self.curr_player == Player.White else Player.White
                    ):
                        capt_pos = Vector2(new_pos.x + dir.x, new_pos.y + dir.y)
                        if (
                            self.__validate_indexes(capt_pos)
                            and self.board[capt_pos.x][capt_pos.y] == Player.Empty
                        ):
                            possible_moves.append(capt_pos)

        return possible_moves

    def all_possible_moves(self) -> list[(Vector2, Vector2)]:
        all_possible_moves = []

        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == self.curr_player:
                    for move in self.__possible_moves(Vector2(x, y)):
                        all_possible_moves.append((move, Vector2(x, y)))

        return all_possible_moves

    def play_turn(self, old_pos: Vector2, new_pos: Vector2) -> None:
        self.__move_checker(old_pos, new_pos)
        self.__score_king(new_pos)
        self.__update_game_end()
        self.tour_count += 1
        if not self.is_end_game:
            self.__change_turn()
