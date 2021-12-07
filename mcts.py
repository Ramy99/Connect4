#Monte Carlo Tree Search Testing
import numpy as np
import np_bitboard as bb

class node:
    def __init__(self, state, visits, parent):
        self.state = state
        self.visits = 0
        self.parent = parent

class mcts:
    def __init__(self, board):
        self.board = board
        self.root = tuple()
        self.tree = {self.root:{}}
