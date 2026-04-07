import random

class Dice:
    def __init__(self):
        self.dice = None
        self.lock_list = None

    def reroll(self):
        for i in range(5):
            if self.lock_list[i] == 0:
                self.dice[i] = random.randint(1,6)
        self.dice.sort()

    def initialize(self):
        self.dice = sorted([random.randint(1,6) for _ in range(5)])
        self.lock_list = [0,0,0,0,0]

    def display(self):
        return list(self.dice)
    
    def lock(self, lock_list):
        self.lock_list = lock_list