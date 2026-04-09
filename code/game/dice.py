import random
import numpy as np

class Dice:
    def __init__(self):
        self.dice = None
        self.lock_list = None

    def reroll(self):
        for i in range(5):
            if self.lock_list[i] == 0:
                self.dice[i] = random.randint(1,6)
        self.dice = np.sort(self.dice)

    def initialize(self):
        self.dice = np.random.randint(1, 7, size=5)
        self.dice = np.sort(self.dice)
        self.lock_list = np.zeros(5)

    def display(self):
        return self.dice
    
    def lock(self, lock_list):
        self.lock_list = lock_list