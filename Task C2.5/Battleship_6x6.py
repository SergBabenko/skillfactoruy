from random import randint, shuffle
import os

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Shot out of bounds!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "You already shot here!"

class BoardWrongShipException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class Ship:
    def __init__(self, stern, length, direction):
        self.stern = stern
        self.length = length
        self.direction = direction
        self.hp = length
        self._dots = self._generate_dots()

    def _generate_dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.stern.x
            cur_y = self.stern.y
            if self.direction == 0:
                cur_x += i
            else:
                cur_y += i
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    @property
    def dots(self):
        return self._dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count_destroyed = 0
        self.field = [["◯"] * size for _ in range(size)]
        self.ships = []
        self.occupied = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.occupied:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "◆"
            self.occupied.append(d)
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
                ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not self.out(cur) and cur not in self.occupied:
                    if verb:
                        self.field[cur.x][cur.y] = "●"
                    self.occupied.append(cur)

    def out(self, d):
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.occupied:

            if self.field[d.x][d.y] in ["X", "●"]:
                raise BoardUsedException()

        self.occupied.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.hp -= 1
                self.field[d.x][d.y] = "X"
                if ship.hp == 0:
                    self.count_destroyed += 1
                    self.contour(ship, verb=True)
                    print("Ship destroyed!")
                    return False
                else:
                    print("Ship was hit!")
                    return True

        self.field[d.x][d.y] = "•"
        print("Miss!")
        return False

    def __str__(self):
        res = "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            line = f" {i + 1} | " + " | ".join(row) + " |"
            if self.hid:
                line = line.replace("◆", "◯")
            res += f"\n{line}"
        return res


# --- Игроки ---
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def __init__(self, board, enemy):
        super().__init__(board, enemy)
        # Список всех клеток для умного выбора без повторов
        self.available_moves = [Dot(x, y) for x in range(6) for y in range(6)]
        shuffle(self.available_moves)

    def ask(self):
        d = self.available_moves.pop()
        print(f"Move Computer: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            coords = input("You move: ").split()
            if len(coords) != 2:
                print("Enter 2 coordinates!")
                continue
            x, y = coords
            if not (x.isdigit() and y.isdigit()):
                print("Enter numbers!")
                continue
            return Dot(int(x) - 1, int(y) - 1)


# --- Логика игры ---
class Game:
    def __init__(self, size=6):
        self.size = size
        self.pl = self.create_board()
        self.co = self.create_board()
        self.co.hid = True
        self.ai = AI(self.co, self.pl)
        self.us = User(self.pl, self.co)

    def create_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        while True:
            board = Board(size=self.size)
            attempts = 0
            for l in lens:
                while True:
                    attempts += 1
                    if attempts > 1000:
                        break
                    ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                    try:
                        board.add_ship(ship)
                        break
                    except BoardWrongShipException:
                        pass
                if attempts > 1000:
                    break
            else:
                board.occupied = []
                return board

    def print_boards(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("-" * 54)
        print("        Player Board                    Computer Board")
        p_lines = str(self.pl).split('\n')
        c_lines = str(self.co).split('\n')
        for p, c in zip(p_lines, c_lines):
            print(f"{p}    {c}")
        print("-" * 54)

    @staticmethod
    def greet():
        """Creating a greeting."""
        print("-------------------")
        print("Welcome to the game")
        print("    BattleShip     ")
        print("-------------------")
        print(" Input format: x y ")
        print("  x - line number  ")
        print(" y - Column number ")
        print("-------------------")

    def loop(self):
        step = 0
        while True:
            self.print_boards()
            if step % 2 == 0:
                print("Move Player!")
                repeat = self.us.move()
            else:
                print("Move Computer!")
                repeat = self.ai.move()

            if repeat:
                step -= 1

            if self.co.count_destroyed == len(self.co.ships):
                self.print_boards()
                print("Player win!")
                break
            if self.pl.count_destroyed == len(self.pl.ships):
                self.print_boards()
                print("Computer win!")
                break
            step += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()