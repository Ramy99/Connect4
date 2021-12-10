#Will Shayne
#CS21
#Connect 4 using numpy uint64s as bitboards

import numpy as np

#base board class for connect4 style games
class bitboard():

    def __init__(self, board_1 = 0, board_2 = 0, rows = 6, cols = 7, in_row = 4):
        #set initial values and board state for class instance
        self.board_1 = np.uint64(board_1)
        self.board_2 = np.uint64(board_2)
        self.board_height = rows + 1
        self.rows = rows
        self.cols = cols
        self.in_row = in_row
        self.count_cols()
        self.end = False
        self.winner = 0
        self.piece_1 = 'X'
        self.piece_2 = 'O'

    #method to add a piece to the board given the player and column id, returns a new class instance
    def add_piece(self, player, col):
        #the variable add is a single bit shifted by the number of the square on the board being added to
        add = np.uint64(1 << (col * self.board_height + self.col_counts[col]))

        #using bitwise or, the new bit is added to the board of the given player
        if player == 1:
            board_1 = self.board_1 | add
            board_2 = self.board_2
        if player == 2:
            board_1 = self.board_1
            board_2 = self.board_2 | add

        #return a new instance of the class with an updated board
        return bitboard(board_1 = board_1, board_2 = board_2, rows = self.rows, cols = self.cols, in_row=self.in_row)

    #method to check the state of the game, whether it's over and which player one, updates those values in the board instance
    def check_end(self):
        #use local variables to check without modifying the actual board
        board_1 = self.board_1
        board_2 = self.board_2

        #each integer in the array represents the number of bits to be shifted for a certain type of win
        #1 for horizontal wins, board_height for vertical wins, board_height + or - 1 for diagonal wins
        shifts = np.array([1, self.board_height, self.board_height + 1, self.board_height - 1], dtype = np.uint64)

        #check for any win by each player by shifting the board by the above integer values in_row - 1 times
        for i in range(self.in_row - 1):
            board_1 = board_1 & (board_1 << shifts)
            board_2 = board_2 & (board_2 << shifts)

        #boards are now arrays of integers, if any of them are not 0 that represents a win by that player
        if board_1.any():
            self.end = True
            self.winner = 1
        elif board_2.any():
            self.end = True
            self.winner = 2

        #if neither player has won and there are no legal moves, the game is a draw
        elif self.legal_moves() == []:
            self.end = True

    #method to count the number of pieces in each column on the board and save those values to a list in the board object
    def count_cols(self):

        #store an integer representing every piece on the board
        board = self.board_1 | self.board_2
        counts = []

        #iterate through each column
        for col in range(self.cols):

            #lower h until there is a piece at that height in the column being searched or the height is 0, then save that height in a list
            h = self.rows
            while h != -1 and board & np.uint64(1 << (h + col * self.board_height)) == 0:
                h -= 1
            counts.append(h+1)
            
        #save that list as a variable inside the class instance
        self.col_counts = counts
    
    #method to return a list of the columns that it is legal to play in given the current board state
    def legal_moves(self):
        return [i for i in range(self.cols) if self.col_counts[i] < self.rows]
    
    #method to return a human-readable representation of the board
    def print_board(self):

        boardlist = []

        #for loops go through the entire board, by row then column, and check if there's a piece there, then puts the character representing that into a list
        #stores those lists of rows in a list, then formats them with the .join() method to create a human readable board
        for row in range(self.rows):
            row_list = []
            for c in range(self.cols):
                square = np.uint64(1 << (c * self.board_height + row))
                if self.board_1 & square:
                    row_list.append(self.piece_1)
                elif self.board_2 & square:
                    row_list.append(self.piece_2)
                else:
                    row_list.append(' ')
            boardlist.insert(0, row_list)
        for i in range(len(boardlist)):
            boardlist[i] = ' | '.join(boardlist[i])
        boardlist.append(' | '.join([str(i+1) for i in range(self.cols)]))
        return '| ' + ' |\n\n| '.join(boardlist) + ' |'

#testing game function for bitboard
def main():
    play = True
    #main game loop
    while play:
        #setup initial boardstate and player
        board = bitboard()
        player = 1
        #loops until each game is over
        while not board.end:
            print(board.print_board())
            col = None
            #input validation for column selection, doesn't let you choose an illegal column
            while col == None or col not in board.legal_moves():
                try:
                    col = int(input("What col? ")) - 1
                    if col not in board.legal_moves():
                        print("Please enter a legal column")
                except ValueError:
                    print("Please enter a legal column")
            #make the chosen move and check if the game is over
            board = board.add_piece(player, col)
            board.check_end()
            if player == 1:
                player = 2
            else:
                player = 1

        #print results
        print(board.print_board())
        if board.winner == None:
            print("It's a draw!")
        elif board.winner == 1:
            print(f"{board.piece_1}'s win!")
        elif board.winner == 2:
            print(f"{board.piece_2}'s win!")

        #input validated check to play again
        play = input("Would you like to play again? (Y or N) ")
        while play.lower() != 'y' and play.lower() != 'n':
            print("Please enter 'Y' or 'N'")
            play = input("Would you like to play again? (Y or N) ")
        if play.lower() == 'y':
            play = True
        else:
            play = False

if __name__ == "__main__":
    main()