import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import np_bitboard as bb

def build_model():
    model = keras.Sequential(
        [
            layers.Input(shape=(2,7,7)),
            layers.Flatten(),
            layers.Dense(128, activation = 'relu'),
            layers.Dense(64, activation = 'relu'),
            layers.Dense(7, activation = 'softmax')
        ]
    )
    return model

class agent:
    def __init__(self, build_func = build_model, play_model = None, target_model = None, loss_func = keras.losses.Huber(), opt = keras.optimizers.Adam(), gamma = .75):
        if play_model != None:
            self.play_model = play_model
        else:
            self.play_model = build_func()
        if target_model != None:
            self.target_model = target_model
        else:
            self.target_model = build_func()
        self.loss_function = loss_func
        self.optimizer = opt
        self.gamma = gamma

    def train_player(self, states, actions, rewards):
        updated_q_values = rewards + self.gamma * tf.reduce_max(self.target_model(states), axis = 1)
        action_masks = tf.one_hot(actions, 7)
        with tf.GradientTape() as tape:
            probs = self.play_model(states)
            prob_action_taken = tf.multiply(probs, action_masks)
            q_action = tf.reduce_sum(prob_action_taken, axis=1)
            loss = self.loss_function(updated_q_values, q_action)
        grads = tape.gradient(loss, self.play_model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.play_model.trainable_variables))
    
    def update_target(self):
        self.target_model.set_weights(self.play_model.get_weights())

    def choose_action(self, state):
        return tf.argmax(self.play_model(state.reshape(1, 2, 7, 7))[0]).numpy()

class memory:
    def __init__(self):
        self.reset()
    def reset(self):
        self.states = []
        self.actions = []
        self.rewards = []
    def step(self, state, action, reward):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)

player_1 = agent()
player_mem = memory()
env = bb.np_bitboard()
training_games = 100
epsilon = 1
epsilon_step = .955

for i in range(training_games):
    env.reset()
    state = env.state()
    player_mem.reset()
    epsilon *= epsilon_step
    while not env.done:
        if env.current_player() == 1:
            if epsilon < np.random.rand(1)[0]:
                action = player_1.choose_action(state)
            else:
                action = np.random.choice(env.legal_moves())
            env.make_move(action)
            if env.win:
                reward = 20
            else:
                reward = 0
            player_mem.step(state, action, reward)
        else:
            action = np.random.choice(env.legal_moves())
            env.make_move(action)
            if env.win:
                player_mem.rewards[-1] = -20
        state = env.state()
    player_1.train_player(np.array(player_mem.states), np.array(player_mem.actions), np.array(player_mem.rewards))
    if (i + 1) % 5 == 0:
        player_1.update_target()
    print(state)
