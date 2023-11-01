from constants import Player


class UI:
    def __init__(self) -> None:
        pass

    def read_checkboard_size(self) -> int:
        while True:
            try:
                size = int(input("Prosze o podanie rozmiaru szachownicy: "))
            except ValueError:
                print("Nieprawidłowy typ danych, spróbuj ponownie...")
            else:
                return size

    def draw_checkboard(
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
