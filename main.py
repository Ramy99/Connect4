#Will Shayne
#CS21
#Main game program, handles user input for connect 4 vs other humans and the ai

import mcts
import bitboard

#function to play a game vs another human
def play_game():
    #setup initial board
    board = bitboard.bitboard()
    turn = 0
    #game loop
    while not board.end:
        #print the board
        print(board.print_board())
        #check the active player, then increment the turn counter
        player = turn % 2 + 1
        turn += 1
        #get the player's move and make it, then check if the game is over
        col = get_move(board)
        board = board.add_piece(player, col)
        board.check_end()
    #print the final board state and winner
    print(board.print_board())
    if board.winner == 0:
        print("It's a draw!")
    else:
        print(f"Player {board.winner} wins!")

#function to play a game vs the ai
def vs_ai(ai_player, human_player):
    #setup initial board
    board = bitboard.bitboard()
    turn = 0
    #game loop
    while not board.end:
        #print the board
        print(board.print_board())
        #set active player then increment the turn counter
        player = turn % 2 + 1
        turn += 1
        #if it's the AI's turn, calculate the best move
        if player == ai_player:
            root = mcts.mcts(board, ai_player, human_player)
            col = root.choose_move()
        #if it's the player's turn, ask them for a move
        if player == human_player:
            col = get_move(board)
        #make the requested move and check if the game is over
        board = board.add_piece(player, col)
        board.check_end()
    #print final board state and winner
    print(board.print_board())
    if board.winner == ai_player:
        print("The computer wins!")
    elif board.winner == human_player:
        print("You win!")
    else:
        print("It's a draw!")

#function to get a valid column number as an input
def get_move(board):
    good_in = False
    #input validation loop
    while not good_in:
        try:
            #board indexes columns at 0, but humans generally count from 1, so this modifies the index to match
            col = int(input("Which column would you like to place a piece in? ")) - 1
            if col in board.legal_moves():
                good_in = True
            else:
                print("Please choose a legal column")
        except ValueError:
            print("Please enter the column as an integer")
    return col

#function to print the main options menu
def print_main_menu():
    print("How would you like to play?")
    print("1. Versus another human")
    print("2. Versus the computer")

def main():
    #set main loop condition to True
    play = True
    #constant list of valid main menu options
    OPTIONS = ["1", "2", "q"]
    #main loop
    while play:
        good_opt = False
        #input validation for menu selection
        while not good_opt:
            print_main_menu()
            choice = input("Enter the number for how you'd like to play, or q to quit: ")
            if choice.lower() in OPTIONS:
                good_opt = True
            else:
                print(f"{choice} is not a valid menu option")
        if choice == "1":
            play_game()
        elif choice == "2":
            print("Would you like to go first or second?")
            player = 0
            while player != "1" and player != "2":
                player = input("Please enter 1 or 2 for first or second: ")
            if player == "1":
                vs_ai(2, 1)
            else:
                vs_ai(1, 2)
        elif choice.lower() == "q":
            play = False

main()