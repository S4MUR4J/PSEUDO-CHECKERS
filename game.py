# Author: Maciej Mucha

# game.py Reprazentacja problemu wykonana za pomocą klasy gry
# odpowiadającą za przechowywanie informacji na temat rozgrywki
# i wykonywanie operacji na niej

from copy import deepcopy

from constants import Directions, Player, Points, Vector2


class Game:
    # Dane parametryzowane
    board_size: int = None
    max_moves: int = None

    # Dane niezależne od parametrów
    board: list[list[Player]] = None
    curr_player: Player = None
    is_end_game: bool = None
    tour_count: int = None
    must_move_checker: Vector2 = None
    move_counter: int = None
    move_history: list[str] = [""]

    white_score: int = None
    red_score: int = None

    # Funkcji inicjującej obiekt uzupełniam informacje na temat rozgrywki
    def __init__(self, size: int = 8, max_moves: int = 1000) -> None:
        self.board_size = size
        self.max_moves = max_moves
        self.move_counter = 0
        self.__fill_board()
        self.curr_player = Player.White
        self.is_end_game = False
        self.white_score = 0
        self.red_score = 0
        self.tour_count = 0
        self.list_string = []

    # Funkcja tworząca warcabnice i uzupełniająca ją warcabami
    def __fill_board(self) -> None:
        self.board = []

        # Logika dostosowująca pusty środek warcabnicy w zależności od rozmiaru
        middle = round(self.board_size / 2)
        empty_rows = [middle, middle - 1]
        if self.board_size % 2 != 0:
            empty_rows.append(middle + 1)

        # Wstawianie warcab na odpowiednie pozycje
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

    # Funkcja zwracająca szczegółową kopie obiektu gry
    def deep_copy(self):
        return deepcopy(self)

    # Funkcja walidująca czy pozycja znajduje się na warcabnicy
    def __validate_indexes(self, new_pos: Vector2) -> bool:
        return 0 <= new_pos.x < self.board_size and 0 <= new_pos.y < self.board_size

    # Funkcja dodająca punkt graczowi, którego tura jest aktualnie
    def __score_player(self, points: Points):
        if self.curr_player == Player.White:
            self.white_score += points.value
        else:
            self.red_score += points.value

    # Funkcja sprawdzająca czy konkretny ruch jest ruchem przejmującym
    def __is_capture_move(self, old_pos: Vector2, new_pos: Vector2) -> bool:
        return abs(old_pos.x - new_pos.x) > 1

    # Funkcja obsługująca przejęcie warcaba, usunięcie go i dodanie punktów za ruch
    def __capture_checker(self, old_pos: Vector2, new_pos: Vector2) -> None:
        capt_pos = Vector2((old_pos.x + new_pos.x) // 2, (old_pos.y + new_pos.y) // 2)
        self.board[capt_pos.x][capt_pos.y] = Player.Empty
        self.__score_player(Points.Capture)

    # Funkcja sprawdzająca czy warcab po ruchu przemienia się w damkę
    def __is_king_transform(self, pos: Vector2) -> bool:
        return (self.curr_player == Player.White and pos.x == self.board_size - 1) or (
            self.curr_player == Player.Red and pos.x == 0
        )

    # Funkcja znikająca i punktująca przemianę w damkę
    def __transform_king(self, pos: Vector2) -> None:
        self.board[pos.x][pos.y] = Player.Empty
        self.__score_player(Points.King)

    # Funkcja przenosząca warcab z starej pozycji na nową
    def __move_checker(self, old_pos: Vector2, new_pos: Vector2) -> None:
        if self.__is_capture_move(old_pos, new_pos):
            self.__capture_checker(old_pos, new_pos)

        self.board[old_pos.x][old_pos.y] = Player.Empty
        self.board[new_pos.x][new_pos.y] = self.curr_player
        self.move_history.append(
            f"{self.curr_player.name}: {chr(65 + self.board_size - old_pos.y - 1)}{old_pos.x + 1} -> {chr(65 + self.board_size - new_pos.y - 1)}{new_pos.x + 1} \n"
        )

        if self.__is_king_transform(new_pos):
            self.__transform_king(new_pos)

    # Funkcja zmieniająca turę, i zwiększająca ilość wykonanych ruchów
    def __change_turn(self) -> None:
        self.move_counter += 1
        self.curr_player = (
            Player.Red if self.curr_player == Player.White else Player.White
        )

    # Funkcja sprawdzająca czy warcab po przejęciu może dokonać kolejnego przejęcia
    def __is_next_capture_possible(self, pos: Vector2) -> bool:
        possible_moves = self.__possible_moves(pos)
        for move in possible_moves:
            if abs(move.x - pos.x) > 1:
                return True

        return False

    # Funkcja sprawdzająca czy na planszy znaduję się warcab, który musi wykonać
    # przejęcie - (jeśli jest możliwość bicia to jeden z warcab musi wykonać taki ruch)
    def __capture_duty(self) -> bool:
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == self.curr_player:
                    if self.__can_capture(Vector2(x, y)):
                        return True

    # Funkcja sprawdzająca czy dany warcab ma możliwość przejęcia
    def __can_capture(self, pos: Vector2) -> bool:
        directions = Directions().get()
        for dir in directions:
            next_pos = Vector2(pos.x + dir.x, pos.y + dir.y)
            if self.__validate_indexes(next_pos):
                if self.board[next_pos.x][next_pos.y] == (
                    Player.Red if self.curr_player == Player.White else Player.White
                ):  # jeśli w zasięgu warcaba znajduję się przeciwny warcab
                    capt_pos = Vector2(next_pos.x + dir.x, next_pos.y + dir.y)
                    if (
                        self.__validate_indexes(capt_pos)
                        and self.board[capt_pos.x][capt_pos.y] == Player.Empty
                    ):  # i tym kierunku dalej jest puste pole
                        return True
        return False

    # Funkcja sprawdzająca czy istnieją jeszcze warcaby obydwu graczy jeśli nie, koniec rozgrywki
    def __are_checkers_on_board(self) -> None:
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

        self.is_end_game = True

    # Funkcja zwracająca możliwe ruchy podanego warcaba bierze również
    def __possible_moves(
        self, pos: Vector2, must_capture: bool = False
    ) -> list[Vector2]:
        possible_moves = []
        directions = Directions().get()

        if self.board[pos.x][pos.y] == self.curr_player:
            for dir in directions:
                new_pos = Vector2(pos.x + dir.x, pos.y + dir.y)
                if self.__validate_indexes(new_pos):
                    if (
                        self.board[new_pos.x][new_pos.y]
                        == Player.Empty  # Pozycja jest pusta
                        and (
                            (self.curr_player == Player.White and dir.x > 0)
                            or (self.curr_player == Player.Red and dir.x < 0)
                        )  # Gracz idzie do "przodu"
                        and not must_capture  # Jeśli nie ma wymuszania ruchu
                    ):
                        possible_moves.append(new_pos)
                    elif self.board[new_pos.x][new_pos.y] == (
                        Player.Red if self.curr_player == Player.White else Player.White
                    ):  # Jeśli wymuszane bicie
                        capt_pos = Vector2(new_pos.x + dir.x, new_pos.y + dir.y)
                        if (
                            self.__validate_indexes(capt_pos)
                            and self.board[capt_pos.x][capt_pos.y] == Player.Empty
                        ):  # Jeśli pozycja znajduje się na warcabnicy i możliwy ruch
                            possible_moves.append(capt_pos)

        return possible_moves

    # Funkcja zwraca wszystkie możliwe do wykonania ruchy przez aktualnego gracza
    def all_possible_moves(self) -> list[(Vector2, Vector2)]:
        all_possible_moves = []
        must_capture = self.__capture_duty()

        # Wykorzystywane w przypadkach gdy mamy kilkukrotne przejęcia sprawdzany tylko konkretny
        if self.must_move_checker is not None:
            for move in self.__possible_moves(self.must_move_checker, must_capture):
                all_possible_moves.append((move, self.must_move_checker))
        # Znajdowanie ruchów każdego warcaba aktualnego gracza pośrednio przez funkcje __possible_moves
        else:
            for x in range(self.board_size):
                for y in range(self.board_size):
                    if self.board[x][y] == self.curr_player:
                        for move in self.__possible_moves(Vector2(x, y), must_capture):
                            all_possible_moves.append((move, Vector2(x, y)))

        # Jeśli brak ruchów gracza to koniec gry dla kilkukrotnych przejęć nie wołamy funkcji
        # ten warunek sprawdzany tylko dla "pierwszego ruchu gracza"
        if len(all_possible_moves) == 0:
            self.is_end_game = True

        return all_possible_moves

    # Funkcja wywołująca szeregu akcji związanych z rozegraniem tury
    def play_turn(self, old_pos: Vector2, new_pos: Vector2) -> None:
        self.__move_checker(old_pos, new_pos)  # Wykonanie ruchu
        self.__are_checkers_on_board()  # Sprawdzenie czy istnieją warcaby gracza

        if self.is_end_game:
            return

        # Jeśli wykonane przejęcie i następne możliwe
        if abs(old_pos.x - new_pos.x) > 1 and self.__is_next_capture_possible(new_pos):
            self.must_move_checker = new_pos
        else:
            self.must_move_checker = None
            self.__change_turn()

    # Funkcja zwraca ocenę stanu planszy na konkretnego gracza
    def get_player_rating(self, player: Player) -> int:
        if player == Player.White:
            return self.white_score  # - self.red_score
        else:
            return self.red_score  # - self.white_score


# EOF
