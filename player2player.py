import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from functools import partial


def announce_winner(player):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Player"+str(player)+"Wins")
    msg.setWindowTitle("Game Over")
    msg.buttonClicked.connect(startgame)
    msg.exec_()
    msg.show()


def check_winner(GSM, depth, move):
    if move < 7:
        return 0
    if move % 2 == 0:
        player = 2
    else:
        player = 1
    for y in range(5, depth-1, -1):
        for x in range(5):
            try:
                if GSM[y][x] == player and GSM[y][x+1] == player and GSM[y][x+2] == player and GSM[y][x+3] == player:
                    announce_winner(player)
                if depth < 3:
                    if GSM[y][x] == player and GSM[y+1][x] == player and GSM[y+2][x] == player and GSM[y+3][x] == player:
                        announce_winner(player)
                    if GSM[y][x] == player and GSM[y+1][x-1] == player and GSM[y+2][x-2] == player and GSM[y+3][x-3] == player:
                        announce_winner(player)
                    if GSM[y][x] == player and GSM[y+1][x+1] == player and GSM[y+2][x+2] == player and GSM[y+3][x+3] == player:
                        announce_winner(player)
            except IndexError:
                break


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
    check_winner(GSM, depth, move)
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


def startgame():
    move_no = 0
    depth = 5
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(1000, 1000)
    w.setWindowTitle("Guru99")

    for y in range(5, -1, -1):
        for x in range(7):
            GAME_BOARD[y][x] = QPushButton(w)
            GAME_BOARD[y][x].setGeometry(200, 150, 100, 100)
            GAME_BOARD[y][x].setStyleSheet(
                "QPushButton""{""background-color : grey;border-radius : 50;border : 2px solid black""}")
            # "border-radius : 50;border : 2px solid black;"
            GAME_BOARD[y][x].move((40+75)*x, (40+75)*y)
            GAME_BOARD[y][x].setEnabled(False)
            GAME_BOARD[y][x].show()
            if y == 5:
                GAME_BOARD[y][x].setEnabled(True)
                GAME_BOARD[y][x].clicked.connect(
                    partial(make_move, GSM, y, x, depth, [], move_no))
    w.show()
    sys.exit(app.exec_())


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
# startgame()
