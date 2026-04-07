import random

class RandomPick:
    def __init__(self):
        None

    def choose_action(self, state):
        _, rolls_left, scoreboard_mask = state

        if rolls_left == 0:
            available_placements = [i+1 for i, num in enumerate(scoreboard_mask) if num == 0]
            action = ("score", random.choice(available_placements))

        elif rolls_left > 0:
            action = ("reroll", tuple([random.randint(0,1) for _ in range(5)]))
    
        return action
    
    def update(self, state, action, reward, next_state):
        return None
        

