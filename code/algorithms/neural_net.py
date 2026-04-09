import random
import math
import numpy as np
import itertools
import copy

class NN:
    def __init__(self):
        self.net = {}
        self.gamma = 0.95
        self.lr = 0.01 #1e-5
        self.epsilon = 1
        self.epsilon_decay = 0.999
        self.min_epsilon = 0.05
        self.actions = {}
        self.categories = [
            "ones", "twos", "threes", "fours", "fives", "sixes",
            "one_pair", "two_pair", "three_of_a_kind", "four_of_a_kind",
            "small_straight", "large_straight",
            "full_house", "chance", "yatzy"
            ]
        self.action_to_index = {}
        self.counter = 0
        self.target_net = {}

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
    
    def choose_action(self, state):
        
        X = self.state_to_input(state)
        A1,A2,A3 = self.forward_pass(X)

        self.net["A1"] = A1
        self.net["A2"] = A2
        self.net["A3"] = A3

        actions_index_list = self.available_action_indices(state)

        logits = A3.flatten()
        
        mask = np.full_like(logits, -np.inf)
        mask[actions_index_list] = logits[actions_index_list]
         
        
        if np.random.rand() < self.epsilon:
            action_index = np.random.choice(actions_index_list)
        else:
            action_index = np.argmax(mask) 

        action = self.actions[action_index]

        return action

    def update(self, state, action, reward, next_state):
        
        X = self.state_to_input(state)

        A1 = self.net["A1"] 
        A2 = self.net["A2"] 
        A3 = self.net["A3"]

        dW1, db1, dW2, db2, dW3, db3 = self.backward_pass(X, A1, A2, A3, action, reward, next_state)

        self.update_weights(dW1, db1, dW2, db2, dW3, db3)

    def state_to_input(self, state):
        
        dice, rolls_left, scorecard_mask = state

        dice = np.array(dice)
        scorecard_mask = np.array(scorecard_mask)
        dice_counts = np.bincount(dice, minlength=7)[1:] / 5
        roll_encoding = np.zeros(3)
        roll_encoding[rolls_left] = 1

        x = np.concatenate([dice_counts, roll_encoding, scorecard_mask])
        
        return x.reshape(-1, 1)
    
    def initalize_actions(self):
        self.actions = {}

        i = 0
        
        for p in itertools.product([0, 1], repeat=5):
            self.actions[i] = ("reroll", np.array(p))
            i += 1

        for category in self.categories:
            self.actions[i] = ("score", category)
            i += 1

        self.action_to_index = {
            (a[0], tuple(a[1]) if a[0] == "reroll" else a[1]): i
            for i, a in self.actions.items()
        }

    def available_actions(self, state):
        dice, rolls_left, scorecard_mask = state

        actions = []

        if rolls_left > 0:
            for numbers in itertools.product([0, 1], repeat=5):
                actions.append(("reroll", np.array(numbers)))

        if rolls_left == 0:
            for i in range(len(scorecard_mask)):
                if scorecard_mask[i] == 0:
                    actions.append(("score", self.categories[i]))

        return actions
    
    def available_action_indices(self, state):

        actions = self.available_actions(state)
        
        index_list = []

        for action in actions:
            action_name = (action[0], tuple(action[1]) if action[0] == "reroll" else action[1])
            index_list.append(self.action_to_index[action_name])
        
        return index_list

    def initialize(self):
        
        self.net["W1"] = np.random.normal(0, np.sqrt(2.0 / 24), (128, 24))
        self.net["W2"] = np.random.normal(0, np.sqrt(2.0 / 128), (128, 128))
        self.net["W3"] = np.random.normal(0, np.sqrt(2.0 / 128), (47, 128))

        self.net["b1"] = np.zeros((128,1))
        self.net["b2"] = np.zeros((128,1))
        self.net["b3"] = np.zeros((47,1))

        self.initalize_actions()

        self.target_net = copy.deepcopy(self.net)

    def forward_pass(self, X):

        A1 = self.relu(self.net["W1"] @ X + self.net["b1"])
        A2 = self.relu(self.net["W2"] @ A1 + self.net["b2"])
        A3 = self.net["W3"] @ A2 + self.net["b3"]

        A3 = np.clip(A3, -100, 100)

        return A1,A2,A3
    
    def forward_pass_target(self, X):

        A1 = self.relu(self.target_net["W1"] @ X + self.target_net["b1"])
        A2 = self.relu(self.target_net["W2"] @ A1 + self.target_net["b2"])
        A3 = self.target_net["W3"] @ A2 + self.target_net["b3"]

        #A3 = np.clip(A3, -100, 100)

        return A1,A2,A3
    
    def loss_vector(self, A3, action_index, reward, next_state):
        
        y = self.bellman(next_state, reward)
        #print("SHAPE A3:" + np.shape(A3))
        result = np.zeros_like(A3)
        result[action_index] = A3[action_index] - y

        return result
        
    def bellman(self, next_state, reward):
        self.counter += 1

        if self.counter >= 100:
            self.target_net = copy.deepcopy(self.net)
            self.counter = 0

        X = self.state_to_input(next_state)
        
        _,_,A3 = self.forward_pass_target(X)

        actions_index_list = self.available_action_indices(next_state)

        logits = A3.flatten()
        
        mask = np.full_like(logits, -np.inf)
        mask[actions_index_list] = logits[actions_index_list]
         
        next_Q_max = np.max(mask)

        target = reward + self.gamma * next_Q_max

        print(target)

        return target

    def backward_pass(self, X, A1, A2, A3, action, reward, next_state):
        action_label, dice = action
        if action_label == "reroll":
            action = (action_label, tuple(dice))
        action_index = self.action_to_index[action]

        dA3 = self.loss_vector(A3, action_index, reward, next_state)

        dW3 = dA3 @ A2.T
        db3 = dA3
        dA2 = self.net["W3"].T @ dA3

        dZ2 = dA2 * (A2 > 0)

        dW2 = dZ2 @ A1.T
        db2 = dZ2
        dA1 = self.net["W2"].T @ dA2

        dZ1 = dA1 * (A1 > 0)
        
        dW1 = dA1 @ X.T
        db1 = dZ1

        dW1 = np.clip(dW1, -1, 1)
        dW2 = np.clip(dW2, -1, 1)
        dW3 = np.clip(dW3, -1, 1)
        db1 = np.clip(db1, -1, 1)
        db2 = np.clip(db2, -1, 1)
        db3 = np.clip(db3, -1, 1)
        
        return dW1, db1, dW2, db2, dW3, db3
    
    def backward(self, X, A1, A2, A3, dA3):
        
        dW3 = dA3 @ A2.T
        db3 = dA3
        dA2 = self.net["W3"].T @ dA3

        dZ2 = dA2 * (A2 > 0)

        dW2 = dZ2 @ A1.T
        db2 = dZ2
        dA1 = self.net["W2"].T @ dA2

        dZ1 = dA1 * (A1 > 0)
        
        dW1 = dA1 @ X.T
        db1 = dZ1
        
        return {
            "W1": dW1, "b1": db1,
            "W2": dW2, "b2": db2,
            "W3": dW3, "b3": db3
        }
    
    def update_weights(self, dW1, db1, dW2, db2, dW3, db3):

        self.net["W1"] -= self.lr * dW1
        self.net["b1"] -= self.lr * db1

        self.net["W2"] -= self.lr * dW2
        self.net["b2"] -= self.lr * db2

        self.net["W3"] -= self.lr * dW3
        self.net["b3"] -= self.lr * db3

    def relu(self, x, derivative=False):
        if derivative:
            return x >= 0
        return np.maximum(0,x)

if __name__ == "__main__":
    X = np.array([
        # Dice
        [1], [2], [3], [3], [6],
        # Rolls left
        [2],
        # Scorecard mask
        [0],[0],[1],[0],[1],[0],[1],[0],[0],[0],[1],[0],[1],[0],[1]
    ])

    next_state = np.array([
        # Dice
        [1], [3], [4], [5], [6],
        # Rolls left
        [1],
        # Scorecard mask
        [0],[0],[1],[0],[1],[0],[1],[0],[0],[0],[1],[0],[1],[0],[1]
    ])

    neural_net = NN()
    neural_net.initialize()
   
