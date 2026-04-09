import game
import random
import itertools


class Qlearn:
    def __init__(self):
        self.Q_table = {}
        self.epsilon = 1
        self.epsilon_decay = 0.99999
        self.min_epsilon = 0.05
        self.alpha = 0.2
        self.gamma = 0.95

    def choose_action(self, state):

        actions = self.available_actions(state)
        
        if random.uniform(0,1) < self.epsilon:
            return random.choice(actions)
        
        q_values = self.Q_table.get(state, {})

        highest_q_value = max(q_values.get(action, 0) for action in actions)
        optimal_actions = [action for action in actions if q_values.get(action,0) == highest_q_value]

        return random.choice(optimal_actions)
    
    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        
    def update(self, state, action, reward, next_state):
        if state not in self.Q_table:
            self.Q_table[state] = {}
        if action not in self.Q_table[state]:
            self.Q_table[state][action] = 0

        next_actions = self.available_actions(next_state)
        next_q = self.Q_table.get(next_state, {})

        if next_actions:
            max_q_for_next = max(next_q.get(action,0) for action in next_actions)
        else:
            max_q_for_next = 0

        self.Q_table[state][action] = self.Q_table[state][action] + self.alpha * (reward + self.gamma * max_q_for_next - self.Q_table[state][action])
    
    def available_actions(self, state):
        dice, rolls_left, scorecard_mask = state

        actions = []

        if rolls_left > 0:
            for numbers in itertools.product([0, 1], repeat=5):
                actions.append(("reroll", numbers))

        if rolls_left == 0:
            for i in range(len(scorecard_mask)):
                if scorecard_mask[i] == 0:
                    actions.append(("score", i+1))

        return actions
    
    
    def save_q_table(self, filename):
        with open(filename, "w") as f:
            for state, action_dict in self.Q_table.items():
                f.write(f"{repr(state)}|{repr(action_dict)}\n")

    
    def load_q_table(self, filename):
        q_table = {}

        try:
            with open(filename, "r") as f:
                for line in f:
                    state_str, actions_str = line.strip().split("|")

                    state = eval(state_str)
                    action_dict = eval(actions_str)

                    q_table[state] = action_dict

        except FileNotFoundError:
            print("No saved Q-table found.")
            self.Q_table = {}

        self.Q_table = q_table

    def save_model(self, filename):
        with open(filename, "w") as f:
    
            # training params
            f.write(repr(self.epsilon) + "\n")
            f.write(repr(self.epsilon_decay) + "\n")
            f.write(repr(self.min_epsilon) + "\n")
            f.write(repr(self.alpha) + "\n")
            f.write(repr(self.gamma) + "\n")

    def load_model(self, filename):
        try:
            with open(filename, "r") as f:
                self.epsilon = eval(f.readline().strip())
                self.epsilon_decay = eval(f.readline().strip())
                self.min_epsilon = eval(f.readline().strip())
                self.alpha = eval(f.readline().strip())
                self.gamma = eval(f.readline().strip())

        except FileNotFoundError:
            print("No saved model found.")

        

            
        
