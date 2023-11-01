class UI:
    
    def __init__(self) -> None:
        pass

    def draw_checkboard(self, checkboard : list[list[chr]], checkboard_size: int) -> None:
        for i in range(checkboard_size):
            if i == 0:
                for k in range(checkboard_size):
                    print(f' {chr(65 + k)}', end='')
                print('\n')
            for j in range(checkboard_size):
                print(f'|{str(checkboard[i][j])}', end='')
                if j == checkboard_size - 1:
                    print(f'|  {checkboard_size - 1}')
        print('')