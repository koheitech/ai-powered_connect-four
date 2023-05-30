import random

print("Welcome to Connect Four")
print("-----------------------")

POSSIBLE_LETTERS = ["A", "B", "C", "D", "E", "F", "G"]
GAME_BOARD = [
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""],
    ["", "", "", "", "", "", ""]
]

ROWS = 6
COLS = 7


def printGameBoard():
    print("\n     A    B    C    D    E    F    G  ", end="")
    for x in range(ROWS):
        print("\n   +----+----+----+----+----+----+----+")
        print(x, " |", end="")
        for y in range(COLS):
            if (GAME_BOARD[x][y] == "🔵"):
                print("", GAME_BOARD[x][y], end=" |")
            elif (GAME_BOARD[x][y] == "🔴"):
                print("", GAME_BOARD[x][y], end=" |")
            else:
                print(" ", GAME_BOARD[x][y], end="  |")
    print("\n   +----+----+----+----+----+----+----+")


def modifyGameBoard(coordinate, chip):
    """
    Based on the parced corrdinate and chip, modify the GAME_BOARD array
    """
    GAME_BOARD[coordinate[0]][coordinate[1]] = chip


def checkForWinner(chip):
    """
    Check any 4 seqquenciak chip in horizontal, vertical and diagonal spaces for both of the players.
    If there is winner, return True. 
    Otherwise, return False.
    """
    # Check horizontal spaces
    for x in range(ROWS):
        for y in range(COLS - 3):
            if GAME_BOARD[x][y] == chip and GAME_BOARD[x][y+1] == chip and GAME_BOARD[x][y+2] == chip and GAME_BOARD[x][y+3] == chip:
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check vertical spaces
    for y in range(COLS):
        for x in range(ROWS - 3):
            if GAME_BOARD[x][y] == chip and GAME_BOARD[x+1][y] == chip and GAME_BOARD[x+2][y] == chip and GAME_BOARD[x+3][y] == chip:
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check upper right to bottom left diagonal spaces
    for x in range(ROWS - 3):
        for y in range(3, COLS):
            if GAME_BOARD[x][y] == chip and GAME_BOARD[x+1][y-1] == chip and GAME_BOARD[x+2][y-2] == chip and GAME_BOARD[x+3][y-3] == chip:
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True

    # Check upper left to bottom right diagonal spaces
    for x in range(ROWS - 3):
        for y in range(COLS - 3):
            if GAME_BOARD[x][y] == chip and GAME_BOARD[x+1][y+1] == chip and GAME_BOARD[x+2][y+2] == chip and GAME_BOARD[x+3][y+3] == chip:
                print("\nGame over", chip, "wins! Thank you for playing :)")
                return True
    return False


def parseCoordinate(inputString):
    """
    Parse the userinput and calculate the corrdinate for the chip.

    @inputString: coordinate for column (A to G)

    @return: 
    if input is not valid or the given column is full, return False
    if input is valid, return coordinate
    """
    coordinate = [None] * 2
    if (inputString[0] == "A"):
        coordinate[0] = getRow(0)
        coordinate[1] = 0
    elif (inputString[0] == "B"):
        coordinate[0] = getRow(1)
        coordinate[1] = 1
    elif (inputString[0] == "C"):
        coordinate[0] = getRow(2)
        coordinate[1] = 2
    elif (inputString[0] == "D"):
        coordinate[0] = getRow(3)
        coordinate[1] = 3
    elif (inputString[0] == "E"):
        coordinate[0] = getRow(4)
        coordinate[1] = 4
    elif (inputString[0] == "F"):
        coordinate[0] = getRow(5)
        coordinate[1] = 5
    elif (inputString[0] == "G"):
        coordinate[0] = getRow(6)
        coordinate[1] = 6
    else:
        return False

    if coordinate[0] == None:
        return False

    return coordinate


def getRow(col):
    """
    Based on the given column, calculate the row of the coordinate.
    Since there is gravity factor in connect for, chip has to be fallen to the bottom.
    This function calculates the valid row considering gravity.
    """
    for row in range(ROWS - 1, -1, -1):
        if not GAME_BOARD[row][col]:
            return row
    return None


leaveLoop = False
turnCounter = 0
while (leaveLoop == False):
    if (turnCounter % 2 == 0):
        printGameBoard()
        while True:
            spacePicked = input("\nChoose a space: ")
            coordinate = parseCoordinate(spacePicked)
            if coordinate:
                modifyGameBoard(coordinate, '🔵')
                break
            else:
                print("Not a valid coordinate")
        winner = checkForWinner('🔵')
        turnCounter += 1

    # It's the computers turn
    else:
        while True:
            cpuChoice = random.choice(POSSIBLE_LETTERS)
            cpuCoordinate = parseCoordinate(cpuChoice)
            if cpuCoordinate:
                modifyGameBoard(cpuCoordinate, '🔴')
                break
        turnCounter += 1
        winner = checkForWinner('🔴')

    if (winner):
        printGameBoard()
        break
