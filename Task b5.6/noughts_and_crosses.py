def greet():
    """Creating a greeting."""
    print("-" * 19)
    print("Welcome to the game\n Noughts & Crosses \n"+ "-" * 19)
    print(" Input format: x y \n x - line number  \n y - column number")
    print("-" * 19)

def print_board():
    """Creating a visual field."""
    print("\n   | 0 | 1 | 2 |")
    print(" " + "-" * 15)
    for i, row in enumerate(field): # get index and element
        print(f" {i} | {' | '.join(row)} | ")
        print(" " + "-" * 15)
    print()

def player_move():
    """We ask for input of coordinates for the move"""
    while True:
        cords = input("    Your move: ").split()

        if len(cords) != 2:    # check the length of the coordinates
            print("Please enter 2 coordinate!")
            continue


        if not all(c.isdigit() for c in cords): # checking that the entered numbers
            print("Input numbers!")
            continue

        x, y = map(int, cords)  # convert coordinates into a number

        if not (0 <= x <= 2 and 0 <= y <= 2):  # check the range
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
       symbols = [field[r][c] for r, c in cord]                  # match checking
       if symbols[0] != " " and all(s == symbols[0] for s in symbols):
           return symbols[0]  # return winer simbol

    return None


greet()
field = [[" "] * 3 for i in range(3)]
count = 0

while True:
    """Checking turn order"""
    print_board()
    current_symbol = "X" if count % 2 == 0 else "0"
    print(f"Move {current_symbol}!")

    x, y = player_move()
    field[x][y] = current_symbol
    count += 1

    if win_combo():
        print(f"{print_board()}\n Win {win_combo()}!!!")
        break

    if count == 9:
        print(f"{print_board()}\n 'Draw'!!!!")
        break
