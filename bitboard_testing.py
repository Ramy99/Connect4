class bitboard:
    def __init__(self, board_one = 0, board_two = 0, num_cols = 7, board_height = 7, column_counts = None):
        self.player_1 = board_one
        self.player_2 = board_two
        self.num_cols = num_cols
        self.board_height = board_height
        self.symbol_0 = ' '
        self.symbol_1 = 'X'
        self.symbol_2 = 'O'
        self.column_counts = self.create_col_counts()

    def add_piece(self, player, col):
        add = 1 << (col * self.board_height + self.column_counts[col])
        if player == 1:
            self.player_1 = self.player_1 | add
        else:
            self.player_2 = self.player_2 | add
        self.column_counts[col] += 1

    def check_win(self, player):
        if player == 1:
            testboard = self.player_1
        else:
            testboard = self.player_2
        #test vertical wins, just shift by 3
        if testboard & (testboard << 1) & (testboard << 2) & (testboard << 3):
            return True
        #test horizontal wins, shift by board height 3 times
        elif testboard & (testboard << self.board_height) & (testboard << self.board_height * 2) & (testboard << self.board_height * 3):
            return True
        #test diagonal wins, shift by board height + 1 3 times, then board height - 1 3 times
        elif testboard & (testboard << self.board_height + 1) & (testboard << (self.board_height + 1) * 2) & (testboard << (self.board_height + 1) * 3):
            return True
        elif testboard & (testboard << self.board_height - 1) & (testboard << (self.board_height - 1) * 2) & (testboard << (self.board_height - 1) * 3):
            return True
        else:
            return False

    def print_board(self):
        boardlist = []
        for row in range(self.board_height - 1):
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

    def list_legal_moves(self):
        legal = [i for i in range(self.num_cols) if self.column_counts[i] < self.board_height - 1]
        return legal

    def create_col_counts(self):
        board = self.player_1 | self.player_2
        col_counts = []
        for i in range(self.num_cols):
            h = self.board_height - 1
            while h != 0 and ((1<<(i*self.board_height + h - 1)) & board) == 0:
                h -= 1
            col_counts.insert(i, h)
        return col_counts
            

def get_input(board):
    col = int(input("What column? "))
    while not col in board.list_legal_moves():
        col = int(input("Choose a legal column: "))
    return col

def main():
    b = bitboard()
    to_play = 1
    while True:
        print(b.print_board())
        col = get_input(b)
        b.add_piece(to_play, col)
        if b.check_win(to_play):
            print(b.print_board())
            print(f"Player {to_play} wins!")
            break
        if to_play == 1:
            to_play = 2
        else:
            to_play = 1
