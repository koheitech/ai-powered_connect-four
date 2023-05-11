class Node:
    # provides necessary things for generating trees
    def __init__(self, board, player, depth):
        self.board = board
        self.player = player
        self.depth = depth
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def generate_children(self):
        if self.depth <= 0:
            return

        for col in range(7):
            if self.is_valid_move(col):
                child = Node(self.make_move(col),
                             not self.player, self.depth - 1)
                self.add_child(child)
                child.generate_children()

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, col):
        board = [row[:] for row in self.board]
        for row in range(5, -1, -1):
            if board[row][col] == 0:
                # 1 for player and 2 for computer
                board[row][col] = 1 if self.player else 2
                break
        return board


class Tree:
    # generate tree from Node class
    def __init__(self, board, player, depth_limit):
        self.board = board
        self.player = player
        self.depth_limit = depth_limit
        self.root = Node(self.board, self.player, self.depth_limit)

    def generate_game_tree(self):
        self.root.generate_children()

    def print_tree(self, node, depth=0):
        print(' ' * depth, end='')
        print(f'Player: {1 if node.player else 2}')
        print(' ' * depth, end='')
        print(f'Board: {node.board}')
        for child in node.children:
            self.print_tree(child, depth+1)

    def check_win(self, node):

        for col in range(7):  # check vertical
            tmp = [row[col] for row in node.board]
            for i in range(3):
                if tmp[i:i+4].count(2) == 4:
                    return (True, float('inf'))
                elif tmp[i:i+4].count(1) == 4:
                    return (True, -float('inf'))

        for row in node.board:  # check horizontal
            for i in range(4):
                if row[i:i+4].count(2) == 4:
                    return (True, float('inf'))
                elif row[i:i+4].count(1) == 4:
                    return (True, -float('inf'))

        for row in range(5, 2, -1):  # check upper right line
            for col in range(4):
                count_P = 0
                count_C = 0

                if node.board[row][col] == 0:
                    break

                for i in range(4):
                    if node.board[row-i][col+i] == 0:
                        break
                    elif node.board[row-i][col+i] == 1:
                        count_P = count_P + 1
                    else:
                        count_C = count_C + 1

                if count_C == 4:
                    return (True, float('inf'))
                elif count_P == 4:
                    return (True, -float('inf'))

        for row in range(5, 2, -1):  # check upper left line
            for col in range(3, 7):
                count_P = 0
                count_C = 0

                if node.board[row][col] == 0:
                    break

                for i in range(4):
                    if node.board[row-i][col-i] == 0:
                        break
                    elif node.board[row-i][col-i] == 1:
                        count_P = count_P + 1
                    else:
                        count_C = count_C + 1

                if count_C == 4:
                    return (True, float('inf'))
                elif count_P == 4:
                    return (True, -float('inf'))

        return (False, None)

    def evaluation(self, node):
        evaluation_score = 0
        count_P = 0
        count_C = 0

        for col in range(7):  # evaluate vertical line
            tmp = [row[col] for row in node.board]
            for i in range(3):
                zero_count = tmp[i:i+4].count(0)
                two_count = tmp[i:i+4].count(2)
                one_count = tmp[i:i+4].count(1)

                if zero_count + two_count == 4:
                    if two_count == 3:
                        count_C += 1000
                    else:
                        count_C += two_count

                elif zero_count + one_count == 4:
                    if one_count == 3:
                        count_P += 1000
                    else:
                        count_P += one_count

        if count_P < count_C:
            evaluation_score += count_C * 10
        elif count_P > count_C:
            evaluation_score += count_P * -10

        count_P = 0
        count_C = 0

        for row in node.board:  # evaluate horizontal line
            for i in range(4):
                zero_count = row[i:i+4].count(0)
                two_count = row[i:i+4].count(2)
                one_count = row[i:i+4].count(1)

                if zero_count + two_count == 4:
                    if two_count == 3:
                        count_C += 1000
                    else:
                        count_C += two_count

                elif zero_count + one_count == 4:
                    if one_count == 3:
                        count_P += 1000
                    else:
                        count_P += one_count

        if count_C > count_P:
            evaluation_score += count_C * 10
        elif count_C < count_P:
            evaluation_score += count_P * -10

        count_P = 0
        count_C = 0

        for row in range(5, 2, -1):  # evaluate upper right line
            for col in range(4):
                if node.board[row][col] == 0:
                    break

                else:
                    for i in range(4):
                        if node.board[row-i][col+i] == 0:
                            break
                        elif node.board[row-i][col+i] == 1:
                            count_P = count_P + 1
                        else:
                            count_C = count_C + 1

        if count_P > count_C:
            evaluation_score += count_P * -2
        elif count_P < count_C:
            evaluation_score += count_C * 2
        else:
            evaluation_score += 0

        count_P = 0
        count_C = 0

        for row in range(5, 2, -1):  # evaluate upper left line
            for col in range(3, 7):
                if node.board[row][col] == 0:
                    break

                else:
                    for i in range(4):
                        if node.board[row-i][col-i] == 0:
                            break
                        elif node.board[row-i][col-i] == 1:
                            count_P = count_P + 1
                        else:
                            count_C = count_C + 1

        if count_P > count_C:
            evaluation_score += count_P * -2
        elif count_P < count_C:
            evaluation_score += count_C * 2
        else:
            evaluation_score += 0

        return evaluation_score

    def AlphaBeta_search(self, node, alpha, beta):
        if self.check_win(node)[0]:
            return self.check_win(node)[1]

        if node.depth <= 0:
            return self.evaluation(node)

        if node.player:
            # minimizing layer
            possible_minimum = float('inf')

            for child in node.children:
                value = self.AlphaBeta_search(child, alpha, beta)
                if value < possible_minimum:
                    possible_minimum = value
                    if possible_minimum < beta:
                        beta = possible_minimum
                if beta <= alpha:
                    break

            return possible_minimum

        else:
            # maximizing layer
            possible_maximum = -float('inf')

            for child in node.children:
                value = self.AlphaBeta_search(child, alpha, beta)
                if value > possible_maximum:
                    possible_maximum = value
                    if possible_maximum > alpha:
                        alpha = possible_maximum
                if alpha <= beta:
                    break

            return possible_maximum

    def make_best_move(self, node):
        maximum = -float('inf')
        promise_row = None
        promise_col = None
        alpha = -float('inf')
        beta = float('inf')

        for child in node.children:
            value = self.AlphaBeta_search(child, alpha, beta)
            if maximum <= value:
                maximum = value
                for col in range(7):
                    for row in range(5, -1, -1):
                        if node.board[row][col] == child.board[row][col]:
                            continue
                        elif child.board[row][col] == 1:
                            continue
                        else:
                            promise_row = row
                            promise_col = col

        return (promise_row, promise_col)


class main_body():
    def call_tree(self, board, player, depth_limit):
        tree = Tree(board, player, depth_limit)
        tree.generate_game_tree()
        row, col = tree.make_best_move(tree.root)

        return row, col
