import random
import math

class NN:
    def __init__(self):
        self.net = {}
        self.gamma = 0.95

    def initialize(self):
        
        self.net["W1"] = [[self.he_init(21) for _ in range(21)] for _ in range(128)]
        self.net["W2"] = [[self.he_init(128) for _ in range(128)] for _ in range(128)]
        self.net["W3"] = [[self.he_init(128) for _ in range(128)] for _ in range(47)]

        self.net["b1"] = [0 for _ in range(128)]
        self.net["b2"] = [0 for _ in range(128)]
        self.net["b3"] = [0 for _ in range(47)]

    def forward_pass(self, X):
        
        A1 = self.relu(self.add_vectors(self.matmul(self.net["W1"],X),self.net["b1"]))
        A2 = self.relu(self.add_vectors(self.matmul(self.net["W2"],A1),self.net["b2"]))
        A3 = self.add_vectors(self.matmul(self.net["W3"],A2),self.net["b3"])

        return A1,A2,A3
    
    def calculate_loss(self, output, action_index, reward, next_state):
        #MSE loss
        result = []
        y = self.bellman(next_state)
        for i in range(len(output)):
            if i == action_index:
                result.append(output - y)
            else:
                result.append(0)
        
    def bellman(self, next_state, reward):
        _,_,A3 = self.forward_pass(next_state)
        return reward + self.gamma * max(A3)


    def backward_pass(self, A1, A2, A3):
        action_index = 1
        reward = 50
        next_state = None
        dQ = self.calculate_loss(A3, action_index, reward, next_state)

        return None
    
    def add_vectors(self, a, b):
        return [x+y for x,y in zip(a, b)]

    def matmul(self, W, X):
        result = []
        for row in W:
            entry = sum(w * x for w, x in zip(row, X))
            result.append(entry)
        return result
    
    def dot(self,a,b):
        return sum(x*y for x,y in zip(a,b))
    
    def softmax(self, x):
        max_num = max(x)
        exponated = [math.exp(num-max_num) for num in x ]

        return [num/sum(exponated) for num in exponated]

    def relu(self, x):
        return [max(0,item) for item in x]

    def he_init(self, n_in):
        std = math.sqrt(2.0/n_in)
        return random.gauss(0, std)


if __name__ == "__main__":
    game_state = [
        #dice
        1, 2, 3, 3, 6,

        #rolls left
        2,

        #scorecard mask
        0,0,1,0,1,0,1,0,0,0,1,0,1,0,1
    ]

    neural_net = NN()
    neural_net.initialize()
    print(neural_net.forward_pass(game_state))