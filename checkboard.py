class checkboard: 

    size : int = None
    board : list[list[chr]] = None
    white_turn : bool = None 

    def __init__(self, checkboard_size : int) -> None:
        self.size = checkboard_size
        self.board = self.fill_checkboard()
        self.white_turn = True

    def fill_checkboard(self) -> list[list[chr]]:
        checkboard = []

        middle = round(self.size / 2)
        empty_rows = [middle, middle - 1]
        if self.size % 2 != 0:
            empty_rows.append(middle + 1)

        for i in range(self.size):
            row = []
            for j in range(self.size):
                if (i + j) % 2 == 0 and not any(i in empty_rows for k in empty_rows):
                    if i < self.size / 2:
                        row.append('W')
                    else:
                        row.append('R')
                else:
                    row.append(' ')
            checkboard.append(row)

        return checkboard 
    
    def change_turn(self) -> None:
        self.white_turn = not self.white_turn