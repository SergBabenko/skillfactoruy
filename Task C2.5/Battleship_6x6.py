from random import randint

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

    def __eq__(self, other):    # compare points
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class Ship:
    def __init__(self, stern, health, direction ):
        self.stern = stern
        self.health = health
        self.direction = direction
        self.hpoint = health

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.health):
            dir_x = self.stern.x     # dots shift
            dir_y = self.stern.y

            if self.direction == 0:  # vertical
                dir_x += i
            elif self.direction == 1:  # horizontal
                dir_y += i

            ship_dots.append(Dot(dir_x, dir_y))

        return ship_dots

    def shooter(self, shot):             # check fo hit
        return shot in self.dots

class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.field = [["◯"] * size for _ in range(size)]

        self.damaged_ship = 0

        self.ships = []

        self.occupied = []

    def __str__(self):
        btlfld = ""
        btlfld += "  | 1  | 2  | 3  | 4  | 5  | 6 |"
        for i, row in enumerate(self.field):
            btlfld += f"\n{i + 1 } ⟦ {' ⟧⟦ '.join(row)} ⟧ "

        # Определение того, какое поле показывать (скрытое или полное)
        # Если self.hid истинно, создаем скрытую версию поля
        if self.hid:
            # Заменяем символы кораблей (например, '■') на пустые символы (' ') для скрытия
            # Нужно адаптировать условие под ваши символы в игре
            btlfld = btlfld.replace('◆', "◯")
        return btlfld

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1,-1), (-1,0), (-1,1),
            (0,-1), (0, 0), (0,1),
            (1,-1), (1,0), (1,1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.occupied:
                    if verb:
                        self.field[cur.x][cur.y] = "●"
                    self.occupied.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.occupied:
                raise BoardWrongShipException
        for d in ship.dots:
            self.field[d.x][d.y] = "◆"
            self.occupied.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.occupied:
            raise BoardUsedException()

        self.occupied.append(d)

        for ship in self.ships:
            if ship.shooter(d):
                ship.hpoint -= 1
                self.field[d.x][d.y] = "X"
                if ship.hpoint == 0:
                    self.damaged_ship += 1
                    self.contour(ship, verb=True)
                    print("Ship destroyed!")
                    return False
                else:
                    print("Ship was hit!")
                    return True
        self.field[d.x][d.y] = "●"
        print("Miss!!")
        return False

    def begin(self):
       self.occupied = []

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
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Move computer: {d.x+1}, {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("You move: ").split()

            if len(cords) != 2:
                print("Enter 2 coordinates!")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print("Enter numbers!")
                continue

            x, y = int(x), int(y)

            return Dot(x-1,y-1)

class Game:
    def __init__(self, size=6):
        self.size = size
        self.pl = self.random_board()
        self.co = self.random_board()
        self.co.hid = True

        self.ai = AI(self.co, self.pl)
        self.us = User(self.pl, self.co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        for l in lens:
            while True:
                ship = Ship(Dot(randint(0, self.size),
                                randint(0, self.size)), l,
                            randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    @staticmethod
    def greet():
        """Creating a greeting."""
        print("-" * 19)
        print("Welcome to the game\n     BattleShip     ")
        print("-" * 19)
        print(" Input format: x y \n  x - line number  \n y - Column number ")
        print("-" * 19)

    def print_2fild(self):
        pl_board_str = str(self.pl)
        computer_board_str = str(self.co)
        player_line = pl_board_str.strip().split("\n")
        computer_line = computer_board_str.strip().split("\n")
        col_width = 33
        separator_width = 5
        total_width = 2 * col_width + separator_width

        print("-" * total_width)
        print(f"{'     Player Board':<{col_width}}{'':<{separator_width}}{'   Computer Board':<{col_width}}")
        print("-" * total_width)
        for p_line, c_line in zip(player_line, computer_line):
            print(f"{p_line:<{col_width}}{'':<{separator_width}}{c_line:<{col_width}}")
        print("-" * total_width)

    def loop(self):
        num = 0
        while True:
            self.print_2fild()

            if num % 2 == 0:
                print("Move Player!")
                repeat = self.us.move()
            else:
                print("Move Computer!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.damaged_ship == 7:
                print("-" * 20)
                print("Player win!")
                break

            if self.us.board.damaged_ship == 7:
                print("-" * 20)
                print("Computer win!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    game = Game()
    game.start()