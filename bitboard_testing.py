class bitboard:
    def __init__(self, board_one = 0, board_two = 0, num_cols = 7, board_height = 6, column_counts = None):
        self.player_1 = board_one
        self.player_2 = board_two
        self.num_cols = num_cols
        self.board_height = board_height
        self.symbol_0 = ' '
        self.symbol_1 = 'X'
        self.symbol_2 = 'O'
        if column_counts == None:
            self.column_counts = [0]*self.num_cols
        else: self.column_counts = column_counts
    def add_piece(self, player, col):
        add = 1 << (col * self.board_height + self.column_counts[col])
        if player == 1:
            self.player_1 = self.player_1 | add
        else:
            self.player_2 = self.player_2 | add
        self.column_counts[col] += 1
    def print_board(self):
        boardlist = []
        for row in range(self.board_height):
            row_list = []
            for c in range(self.num_cols):
                square = 1 << (c * self.board_height + row)
                if self.player_1 & square:
                    row_list.append(self.symbol_1)
                elif self.player_2 & square:
                    row_list.append(self.symbol_2)
                else:
                    row_list.append(self.symbol_0)
            boardlist.insert(0, row_list)
        for i in range(len(boardlist)):
            boardlist[i] = ' | '.join(boardlist[i])
        return '| ' + ' |\n\n| '.join(boardlist) + ' |'
