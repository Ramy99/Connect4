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
        return tf.argmax(self.play_model(state.reshape(1, 2, 7, 7))[0]).numpy()

class buffer:
    def __init__(self, size = 1000):
        self.size = size
        self.reset()
    def reset(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.next_states = []
    def save(self, state, action, reward, next_state):
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
        sample_states = np.array([self.states[i] for i in indices])
        sample_actions = [self.actions[i] for i in indices]
        sample_rewards = [self.rewards[i] for i in indices]
        sample_next_states = np.array([self.next_states[i] for i in indices])
        return sample_states, sample_actions, sample_rewards, sample_next_states


player_1 = agent()
play_buffer = buffer()
env = bb.np_bitboard()
training_games = 5000
epsilon = 1
epsilon_step = .999
turns = 0
train_after_turns = 50
update_target_after = 200
training_batch_size = 32

for i in range(training_games):
    env.reset()
    print("New Game")
    while not env.done:
        state = env.state()
        if env.current_player() == 1:
            if epsilon > np.random.rand(1)[0]:
                action = np.random.choice(env.legal_moves())
            else:
                values = player_1.play_model(state.reshape(1,2,7,7))
                action = tf.argmax(values[0]).numpy()
            epsilon *= epsilon_step
            env.make_move(action)
            if env.win:
                reward = 20
            else:
                reward = 0
            next_state = env.state()
            play_buffer.save(state, action, reward, next_state)
            turns += 1
        elif env.current_player() == 2:
            action = np.random.choice(env.legal_moves())
            env.make_move(action)
        if turns % train_after_turns == 0:
            print("Training")
            training_states, training_actions, training_rewards, training_next_states = play_buffer.sample(batch_size=training_batch_size)
            player_1.train_player(training_states, training_actions, training_rewards, training_next_states)
        if turns % update_target_after == 0:
            print("Updating target model")
            player_1.update_target()
player_1.play_model.save('Trained_model')