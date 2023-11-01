from constants import Player, Vector2


class Checkboard: 

    size : int = None
    board : list[list[chr]] = []

    def __init__(self, checkboard_size : int) -> None:
        self.size = checkboard_size
        self.board = self.__fill_checkboard()

    def __fill_checkboard(self) -> list[list[chr]]:
        checkboard = []

        middle = round(self.size / 2)
        empty_rows = [middle, middle - 1]
        if self.size % 2 != 0:
            empty_rows.append(middle + 1)

        for x in range(self.size):
            row = []
            for y in range(self.size):
                if (x + y) % 2 == 0 and not any(x in empty_rows for k in empty_rows):
                    if x < self.size / 2:
                        row.append(Player.White.value)
                    else:
                        row.append(Player.Red.value)
                else:
                    row.append(Player.Empty.value)
            checkboard.append(row)

        return checkboard


    def move_checker(self, old_pos: Vector2, new_pos: Vector2, player : chr) -> None:
        self.board[old_pos.x][old_pos.y] = Player.Empty.value
        self.board[new_pos.x][new_pos.y] = player
