def greet():
    """Creating a greeting."""
    print("-------------------")
    print("Welcome to the game")
    print(" Noughts & Crosses ")
    print("-------------------")
    print(" Input format: x y ")
    print("  x - line number  ")
    print(" y - Column number ")
    print("-------------------")

def print_board():
    """Creating a visual field."""
    print()
    print("   | 0 | 1 | 2 |")
    print(" ---------------")
    for i, row in enumerate(field): # get index and element
        row_str = f" {i} | {' | '.join(row)} | "
        print(row_str)
        print(" ---------------")
    print()

def player_move():
    """We ask for input of coordinates for the move"""
    while True:
        cords = input("    Your move: ").split()

        if len(cords) != 2:    # check the length of the coordinates
            print("Please enter 2 coordinate!")
            continue

        x, y = cords

        if not(x.isdigit()) or not(y.isdigit()): # checking that the entered numbers
            print("Input numbers!")
            continue

        x, y = int(x), int(y)  # convert coordinates into a number

        if 0 > x or x > 2 or 0 > y or y > 2:  # check the range
            print("Coordinate out of range!")
            continue

        if field[x][y] != " ":            # check cell free or occupied
            print("cell is occupied!")
            continue

        return x, y

def win_combo():
    """Creating a win combo."""
    win_cord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for cord in win_cord:
        symbols = []
        for c in cord:                   # match checking
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Win X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Win 0!!!")
            return True
    return False


greet()
field = [[" "] * 3 for i in range(3)]
count = 0
while True:
    """Checking turn order"""
    count += 1
    print_board()
    if count % 2 == 1:
        print("Move Crosses!")
    else:
        print("Move noughts!")

    x, y = player_move()

    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"

    if win_combo():
        break

    if count == 9:
        print("Draw!")
        break

