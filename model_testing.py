import numpy as np
from numpy.core.fromnumeric import size
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
            layers.Dense(7, activation = 'linear')
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

    def train_player(self, states, actions, rewards, next_states):
        updated_q_values = rewards + self.gamma * tf.reduce_max(self.target_model(next_states), axis = 1)
        action_masks = tf.one_hot(actions, 7)
        with tf.GradientTape() as tape:
            q_vals = self.play_model(states)
            q_actions = tf.multiply(q_vals, action_masks)
            q_action = tf.reduce_sum(q_actions, axis=1)
            loss = self.loss_function(updated_q_values, q_action)
        grads = tape.gradient(loss, self.play_model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.play_model.trainable_variables))
    
    def update_target(self):
        self.target_model.set_weights(self.play_model.get_weights())

    def choose_action(self, state):
        return tf.argmax(self.play_model(state.reshape(1, 2, 7, 7))[0])

class buffer:
    def __init__(self, size = 1000):
        self.size = size
        self.reset()
    def reset(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
    def step(self, state, action, reward, next_state):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.next_states.append(next_state)
        if len(self.states) > self.size:
            self.states = self.states[1:]
            self.actions = self.actions[1:]
            self.rewards = self.rewards[1:]
    def sample(self, batch_size = 8):
        indices = np.random.choice(len(self.rewards), size = batch_size, replace = False)
        sample_states = []
        sample_actions = []
        sample_rewards = []
        sample_next_states = []
        for i in indices:
            sample_states.append(self.states[i])
            sample_actions.append(self.actions[i])
            sample_rewards.append(self.actions[i])
            sample_next_states.append(self.next_states[i])
        return sample_states, sample_actions, sample_rewards, sample_next_states


player_1 = agent()
play_buffer = buffer()
env = bb.np_bitboard()
training_games = 100
epsilon = 1
epsilon_step = .955

for i in range(training_games):
    env.reset()
    while not env.done:
        state = env.state()
        