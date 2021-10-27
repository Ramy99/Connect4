#Connect 4 using numpy uint64s as bitboards, output state as numpy arrays

import numpy as np

class np_bitboard():
    def __init__(self, board_1 = 0, board_2 = 0, rows = 6, cols = 7):
        self.board_1 = np.uint64(board_1)
        self.board_2 = np.uint64(board_2)
        self.board_height = rows + 1
        self.rows = rows
        self.cols = cols
        self.count_cols()
        self.turn = 0
        self.done = False
        self.win = False
    def add_piece(self, player, col):
        add = np.uint64(1 << (col * self.board_height + self.col_counts[col]))
        if player == 1:
            self.board_1 = self.board_1 | add
        if player == 2:
            self.board_2 = self.board_2 | add
        self.col_counts[col] += 1
    def check_win(self, player):
        if player == 1:
            board = self.board_1
        if player == 2:
            board = self.board_2
        shifts = np.array([1, 1 << self.board_height, 1 << self.board_height + 1, 1 << self.board_height - 1], dtype = np.uint64)
        for i in range(3):
            board = board & (board << shifts)
        if board.any():
            return True
        else:
            return False
    def state(self):
        comp = np.ones(self.board_height * self.cols, dtype = np.uint64) << np.arange(self.board_height * self.cols, dtype = np.uint64)
        board_array = np.array([comp & self.board_1, comp & self.board_2], dtype = bool)
        board_array = board_array.reshape(2, 7, 7).view(np.uint8)
        return board_array
    def count_cols(self):
        board = self.board_1 | self.board_2
        counts = []
        for col in range(self.cols):
            h = self.rows
            while h != 0 and board & np.uint64(1 << (h + col * self.board_height)) == 0:
                h -= 1
            counts.append(h)
        self.col_counts = counts
    def legal_moves(self):
        return [i for i in range(self.cols) if self.col_counts[i] < self.rows]
    def make_move(self, col):
        if col in self.legal_moves():
            self.add_piece(self.current_player(), col)
            if self.check_win(self.current_player()):
                self.done = True
                self.win = True
            elif self.legal_moves() == []:
                self.done = True
        self.turn += 1
    def current_player(self):
        return self.turn % 2 + 1
    def reset(self):
        self.__init__()
