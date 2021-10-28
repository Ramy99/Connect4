import numpy as np
import tensorflow as tf
from tensorflow import keras
import np_bitboard as bb

trained_model = keras.models.load_model('Trained_model')
env = bb.np_bitboard()

def get_move(board):
    move = int(input("What column? "))
    while move not in board.legal_moves():
        move = int(input("What column? "))
    return move

while not env.done:
    if env.current_player() == 1:
        action = tf.argmax(trained_model(env.state().reshape(1,2,7,7))[0]).numpy()
        env.make_move(action)
        print("Computer played in column", action)
    else:
        print(env.print_board())
        action = get_move(env)
        env.make_move(action)