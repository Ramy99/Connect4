#Will Shayne

import unittest

class Board:
    def __init__(self, board):
        self.board = board
    #function to create an ascii connect 4 board
    def print_board(self):
        s = '---'.join(['+']*9)
        ls = [s]
        for i in range(len(self.board)):
            r = []
            for t in self.board:
                r.append(t[i])
            ls.append(('| ' + ' | '.join(r) + ' |').replace('_', ' '))
        ls.append(s)
        return '\n'.join(ls)
    #function to check if the most recently played square in a column is connected to a win
    def check_winner(self, x_pos):
        
        i = 0
        while i <= 7 and self.board[x_pos][i] == '_':
            i += 1
        if i == 8:
            return False
        s = self.board[x_pos][i]
        #check vertical win
        v_count = 0
        v = i
        while 0<=v<=7 and self.board[x_pos][v] == s:
            v_count += 1
            v += 1
        v = i-1
        while 0<=v<=7 and self.board[x_pos][v] == s:
            v_count += 1
            v -= 1
        if v_count >= 4:
            return True
        #check horizontal win
        h_count = 0
        h = x_pos
        while 0<=h<=7 and self.board[h][i] == s:
            h_count += 1
            h += 1
        h = x_pos - 1
        while 0<=h<=7 and self.board[h][i] == s:
            h_count += 1
            h -= 1
        if h_count >= 4:
            return True
        #check diagonal wins
        d1_count = 0
        x = x_pos
        y = i
        while 0<=x<=7 and 0<=y<=7 and self.board[x][y] == s:
            d1_count += 1
            x += 1
            y += 1
        x = x_pos - 1
        y = i - 1
        while 0<=x<=7 and 0<=y<=7 and self.board[x][y] == s:
            d1_count += 1
            x -= 1
            y -= 1
        if d1_count >=4:
            return True
        d2_count = 0
        x = x_pos
        y = i
        while 0<=x<=7 and 0<=y<=7 and self.board[x][y] == s:
            d2_count += 1
            x += 1
            y -= 1
        x = x_pos - 1
        y = i + 1
        while 0<=x<=7 and 0<=y<=7 and self.board[x][y] == s:
            d2_count += 1
            x -= 1
            y += 1
        if d2_count >= 4:
            return True
        return False
    #function to place a piece on the board, return a new board object
    def add_piece(self, x_pos, player):
        l = list(self.board)
        l[x_pos] = list(l[x_pos])
        i = 0
        while i <= 7 and l[x_pos][i] == '_':
            i += 1
        l[x_pos][i-1] = player
        l[x_pos] = tuple(l[x_pos])
        t = tuple(l)
        return Board(t)

class BoardTest(unittest.TestCase):
    def setUp(self):
        self.board_rows = 8
        self.board_columns = 8
        self.board = Board((('_',)*self.board_rows,)*self.board_columns)
        self.s = 'X'
    def tearDown(self):
        del self.board
    #unit test for Board.check_winner, all possible horizontal arrangements
    def test_horizontal_wins(self):
        for row in range(self.board_rows):
            with self.subTest(row = row):
                for start_col in range(self.board_columns):
                    with self.subTest (start_col = start_col):
                        for end_col in range(start_col, self.board_columns):
                            with self.subTest(end_col = end_col):
                                b = (('_',) * self.board_rows,) * (start_col) + (('_',)*(row) + (self.s,) + ('_',) * (self.board_rows - row - 1),) * (end_col - start_col + 1) +  (('_',) * self.board_rows,) * (self.board_columns - end_col -1)
                                self.board = Board(b)
                                for c in range(self.board_columns):
                                    with self.subTest(col = c):
                                        if end_col - start_col >= 3 and start_col<=c<=end_col:
                                            self.assertTrue(self.board.check_winner(c))
                                        else:
                                            self.assertFalse(self.board.check_winner(c))
                        
    def test_vertical_wins(self):
        for x_start in range(self.board_columns):
            with self.subTest(x_start = x_start):
                for y_start in range(self.board_rows):
                    with self.subTest(y_start = y_start):
                        for length in range(1, self.board_rows - y_start + 1):
                            with self.subTest(length = length):
                                b = (('_',) * self.board_rows,) * x_start + (('_',) * y_start + (self.s,) * length + ('_',) * (self.board_rows - y_start - length),) + (('_',) * (self.board_rows),) * (self.board_columns - x_start - 1)
                                self.board = Board(b)
                                for c in range(self.board_columns):
                                    with self.subTest(column = c,):
                                        if c == x_start and length >= 4:
                                            self.assertTrue(self.board.check_winner(c))
                                        else:
                                            self.assertFalse(self.board.check_winner(c))
                
    #unit test for Board.check_winner, all possible diagonal arrangements
    def test_diagonal_wins(self):
        for x_start in range(self.board_columns):
            with self.subTest(x_start = x_start):
                for y_start in range(self.board_rows):
                    with self.subTest(y_start = y_start):
                        for length in range(1, min(self.board_columns - x_start, self.board_rows - y_start) + 1):
                            with self.subTest(length = length):
                                b = ()
                                for column in range(self.board_columns):
                                    if column >= x_start and column < x_start + length:
                                        b += (('_',) * (column - x_start + y_start) + (self.s,) + ('_',) * (self.board_columns - column - y_start + x_start - 1),)
                                    else:
                                        b += (('_',) * self.board_columns,)
                                self.board = Board(b)
                                for c in range(self.board_columns):
                                    with self.subTest(column = c):
                                        if x_start + length > c >= x_start and length >= 4:
                                            self.assertTrue(self.board.check_winner(c))
                                        else:
                                            self.assertFalse(self.board.check_winner(c))
                        for length in range(1, min(self.board_columns - x_start, y_start + 1) + 1):
                            with self.subTest(length = length):
                                b = ()
                                for column in range(self.board_columns):
                                    if column >= x_start and column < x_start + length:
                                        b += (('_',) * (x_start + y_start - column) + (self.s,) + ('_',) * (self.board_columns - x_start - y_start + column - 1),)
                                    else:
                                        b += (('_',) * self.board_columns,)
                                self.board = Board(b)
                                for c in range(self.board_columns):
                                    with self.subTest(column = c):
                                        if x_start + length > c >= x_start and length >= 4:
                                            self.assertTrue(self.board.check_winner(c))
                                        else:
                                            self.assertFalse(self.board.check_winner(c))
    #unit test for Board.add_piece, all squares
    def test_add_all_squares(self):
        for row in range(1,self.board_rows + 1):
            with self.subTest(row = row):
                for column in range(1,self.board_columns + 1):
                    b = [('_',)*row+('F',)*(self.board_rows-row)]*self.board_columns
                    self.board.board = tuple(b)
                    b[column-1] = ('_',)*(row-1) + (self.s,) + ('F',)*(self.board_rows-row)
                    with self.subTest(column = column):
                        self.assertEqual(self.board.add_piece(column-1, self.s).board, tuple(b))

def get_column(board):
    i = int(input('What column? ')) - 1
    while not 0<=i<=7 or board.board[i][0] != '_':
        print('Pick a valid column')
        i = int(input('What column? ')) - 1
    return i

def main():
    b = Board((('_',)*8,)*8)
    s = 'X'
    while True:
        print(f'{s} to play')
        i = get_column(b)
        b = b.add_piece(i, s)
        print(b.print_board())
        if b.check_winner(i):
            print(f'{s} wins!')
            break
        if s == 'X':
            s = 'O'
        else:
            s = 'X'

unittest.main()
