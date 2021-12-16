#Will Shayne
#CS21

import numpy as np
import time
import bitboard as bb

#Basic monte carlo tree search implementation
class mcts:

    #class wide constant for how long to take each turn
    TIME_LIMIT = 5
    #class wide constant for how deep to run simulations
    SIM_DEPTH = 12

    def __init__(self, state, active_player, next_player, parent = None, action = None):
        #stores given characteristics of the node, and initializes some variables
        self.state = state
        self.parent = parent
        self.action = action
        self.active_player = active_player
        self.next_player = next_player
        self.terminal = self.state.end
        self.actions = self.state.legal_moves()
        self.children = {}
        self.visits = 0
        self.results = {0:0, 1:0, 2:0}
    
    #creates the child of the next legal action, removes it from the list of actions to try, adds the child to the dictionary of children, and returns it
    def expand(self):
        #get the next legal action
        act = self.actions.pop()
        #determine the state after making that action
        child_state = self.state.add_piece(self.active_player, act)
        child_state.check_end()
        #create the child node stored in the dictionary of children
        self.children[act] = mcts(child_state, self.next_player, self.active_player, parent = self, action = act)
        #return the node
        return self.children[act]
    
    #checks if this node is fully expanded (every legal move has a child node associated with it)
    def expanded(self):
        return len(self.actions) == 0
    
    #plays up to sim_depth random moves from the current position or until the game ends, then returns the result of the game
    def simulate(self):
        #setup local variables for simulation
        simulation_state = self.state
        simulation_player = self.active_player
        depth = 0
        #light rollout loop, choosing random moves for each player
        while not simulation_state.end and depth < self.SIM_DEPTH:
            depth += 1
            action = np.random.choice(simulation_state.legal_moves())
            simulation_state = simulation_state.add_piece(simulation_player, action)
            simulation_state.check_end()
            if simulation_player == 1:
                simulation_player = 2
            else:
                simulation_player = 1
        #return the winner, 0 if draw, 1 if player 1 wins, 2 if player 2 wins
        return simulation_state.winner
    
    #updates visit and win counts for self and all nodes above in the tree
    def update_counts(self, result):
        #update self counts
        self.results[result] += 1
        self.visits += 1
        #update parent counts recursively
        if self.parent != None:
            self.parent.update_counts(result)
    
    #chooses a child from the dictionary of children based on the Upper Confidence Bound formula, with optional exploration (not used when finding the best action)
    def select_child(self, exp_param = 2**.5):
        #create a list of the node's children
        children = list(self.children.values())
        #find the index of the child with the highest Upper Confidence Bound
        best = np.argmax([(c.results[self.active_player] - c.results[self.next_player]) / c.visits + exp_param * (np.log(self.visits)/c.visits)**.5 for c in children])
        #return that node
        return children[best]

    #returns a child node that hasn't been simulated, going through the best child nodes if all are already expanded, or self if terminal
    def find_leaf(self):
        current = self
        #loop until the current selected node is terminal
        while not current.terminal:
            if current.expanded():
                #if current node is fully expanded, select a child node and loop
                current = current.select_child()
            else:
                #if current node is not fully expanded, expand it by one action and return the resulting child node
                return current.expand()
        #if resulting node is terminal, return it
        return current
    
    #returns the best move found in the given amount of time
    def choose_move(self):
        start = time.time()
        #find a leaf, run a simulation, then propogate the result back up the tree, repeat until out of time
        while time.time() - start < self.TIME_LIMIT:
            leaf = self.find_leaf()
            winner = leaf.simulate()
            leaf.update_counts(winner)
        #choose the best child without exploration, and return its action
        return self.select_child(exp_param=0).action

#testing function for games vs the ai
def main():
    board = bb.bitboard()
    player = 1
    while not board.end:
        print(board.print_board())
        if player == 1:
            root = mcts(board, 1, 2)
            col = root.best_action().parent_move
        else:
            col = int(input("What column? "))
        board = board.add_piece(player, col)
        board.check_end()
        if player == 1:
            player = 2
        else:
            player = 1

if __name__ == "__main__":
    main()