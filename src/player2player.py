import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from functools import partial


def announce_winner(player):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Player"+str(player)+"Wins")
    msg.setWindowTitle("Game Over")
    msg.buttonClicked.connect(sys.exit)
    msg.exec_()
    msg.show()


def check_winner(GSM, move):

    if move % 2 == 0:
        chip = 2
    else:
        chip = 1
    """
    Check any 4 seqquenciak chip in horizontal, vertical and diagonal spaces for both of the players.
    If there is winner, return True. 
    Otherwise, return False.
    """
    # Check horizontal spaces
    for x in range(ROWS):
        for y in range(COLS - 3):
            if GSM[x][y] == chip and GSM[x][y+1] == chip and GSM[x][y+2] == chip and GSM[x][y+3] == chip:
                announce_winner(chip)

    # Check vertical spaces
    for y in range(COLS):
        for x in range(ROWS - 3):
            if GSM[x][y] == chip and GSM[x+1][y] == chip and GSM[x+2][y] == chip and GSM[x+3][y] == chip:
                announce_winner(chip)

    # Check upper right to bottom left diagonal spaces
    for x in range(ROWS - 3):
        for y in range(3, COLS):
            if GSM[x][y] == chip and GSM[x+1][y-1] == chip and GSM[x+2][y-2] == chip and GSM[x+3][y-3] == chip:
                announce_winner(chip)

    # Check upper left to bottom right diagonal spaces
    for x in range(ROWS - 3):
        for y in range(COLS - 3):
            if GSM[x][y] == chip and GSM[x+1][y+1] == chip and GSM[x+2][y+2] == chip and GSM[x+3][y+3] == chip:
                announce_winner(chip)
    return False


def make_move(GSM, y, x, depth, occupiedCOL, move):

    move += 1
    red = "QPushButton""{""background-color : red;border-radius : 50;border : 2px solid black""}"
    blue = "QPushButton""{""background-color : blue;border-radius : 50;border : 2px solid black""}"
    if move % 2 == 0:
        colour = red
        GSM[y][x] = 2
    else:
        colour = blue
        GSM[y][x] = 1
    GAME_BOARD[y][x].setStyleSheet(colour)
    GAME_BOARD[y][x].setEnabled(False)
    if x not in occupiedCOL:
        occupiedCOL.append(x)
    if y < depth:
        depth = y
    check_winner(GSM, move)
    for y in range(5, depth-1, -1):
        for x in range(7):
            if y == 5 and GSM[y][x] < 1 and (x not in occupiedCOL):
                # GSM[y][x]=-1
                GAME_BOARD[y][x].setStyleSheet(
                    "QPushButton""{""background-color : white;border-radius : 50;border : 2px solid black""}")
                GAME_BOARD[y][x].setEnabled(True)
                GAME_BOARD[y][x].clicked.connect(
                    partial(make_move, GSM, y, x, depth, [], move))
            if GSM[y][x] > 0 and y > 0 and GSM[y-1][x] != 1 and GSM[y-1][x] != 2:
                # GSM[y-1][x]=-1
                GAME_BOARD[y-1][x].setStyleSheet(
                    "QPushButton""{""background-color : white;border-radius : 50;border : 2px solid black""}")
                GAME_BOARD[y-1][x].setEnabled(True)
                GAME_BOARD[y-1][x].clicked.connect(
                    partial(make_move, GSM, y-1, x, depth+1, [], move))


def startgame(w, label, btn1, btn2):
    if label != None:
        label.hide()
        btn1.hide()
        btn2.hide()
    depth = 5
    for y in range(5, -1, -1):
        for x in range(7):
            GAME_BOARD[y][x] = QPushButton(w)
            GAME_BOARD[y][x].setGeometry(200, 150, 100, 100)
            GAME_BOARD[y][x].setStyleSheet(
                "QPushButton""{""background-color : grey;border-radius : 50;border : 2px solid black""}")
            # "border-radius : 50;border : 2px solid black;"
            GAME_BOARD[y][x].move((40+75)*x, (40+75)*y)
            GAME_BOARD[y][x].setEnabled(False)
            GAME_BOARD[y][x].clicked.connect(
                partial(make_move, GSM, y, x, depth, []))
            GAME_BOARD[y][x].show()
            if y == 5:
                GAME_BOARD[y][x].setEnabled(True)
    w.show()


GAME_BOARD = [
    ["a0", "b0", "c0", "d0", "e0", "f0", "g0"],
    ["a1", "b1", "c1", "d1", "e1", "f1", "g1"],
    ["a2", "b2", "c2", "d2", "e2", "f2", "g2"],
    ["a3", "b3", "c3", "d3", "e3", "f3", "g3"],
    ["a4", "b4", "c4", "d4", "e4", "f4", "g4"],
    ["a5", "b5", "c5", "d5", "e5", "f5", "g5"]
]
# Game State Matrix
GSM = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

ROWS = len(GSM)
COLS = len(GSM[0])
