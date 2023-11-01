from constants import Player


class Game:
    curr_player: Player = None
    who_won: Player = None
    is_end_game: bool = None

    def __init__(self) -> None:
        self.curr_player = Player.White
        self.who_won = Player.Empty.value
        self.is_end_game = False

    def change_turn(self) -> None:
        self.curr_player = (
            Player.Red if self.curr_player == Player.White else Player.White
        )

    def update_who_won(self, board: list[list[chr]], checkboard_size: int) -> None:
        any_white_checker = False
        any_red_checker = False

        for x in range(checkboard_size):
            for y in range(checkboard_size):
                if board[x][y] == Player.White.value:
                    any_white_checker = True
                elif board[x][y] == Player.Red.value:
                    any_red_checker = True

                if any_white_checker and any_red_checker:
                    return

        self.who_won = Player.White if any_white_checker == True else Player.Red
        self.is_end_game = True
