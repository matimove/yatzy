import random
from game.dice import Dice
from game.scoreboard import Scoreboard
import numpy as np

class Yatzy:
    def __init__(self):
        self.state = True
        
        self.lock_list = np.array([0,0,0,0,0])
        self.printouts = False
        self.dice = Dice()
        self.dice.initialize()
        self.scoreboard = Scoreboard()
        self.scoreboard.initialize()
        self.rolls_left = 2
        self.reward = 0
        self.done = 0
        self.next_state = None
        self.final_score = 0
        self.upper_sum = 0
        self.info = 0
        self.print = False
       

    def reset(self):
        self.state = True
        self.lock_list = np.array([0,0,0,0,0])
        self.dice.initialize()
        self.scoreboard.initialize()
        self.rolls_left = 2
        self.reward = 0
        self.done = False
        self.next_state = None
        self.final_score = 0
        self.upper_sum = 0
        self.info = 0
        
        
        return (tuple(self.dice.display()), self.rolls_left, tuple(self.scoreboard.get_scoreboard_mask()))
    
    def step(self, action):

        if action[0] == "reroll":
            self.rolls_left -= 1
            if self.rolls_left < 0:
                raise ValueError('rolls_left went negative!')
            
            old_dice = self.dice.display()

         
            lock_mask = action[1]
            self.dice.lock(lock_mask)
            self.dice.reroll()

        elif action[0] == "score":
            placement = action[1]
            self.scoreboard.place_score(self.dice, placement)
            self.dice.lock([0,0,0,0,0])
            self.dice.reroll()
            self.rolls_left = 2
            old_dice = self.dice.display()

        self.generate_reward(action, old_dice)
        
        self.check_if_game_over()

        #Is bellman working correctly at the end of the game?
        self.next_state = (tuple(self.dice.display()), self.rolls_left, tuple(self.scoreboard.get_scoreboard_mask()))

        return self.next_state, self.reward, self.done, self.final_score, self.info

    def generate_reward(self, action, old_dice):
        
        self.reward = 0

        if action[0] == "score":
            
            self.reward += self.scoreboard.place_score(self.dice, action[1])

            if self.reward == 0:
                self.reward = -5

        self.reward += 0.3 * (self.dice_strength(self.dice.display()) - self.dice_strength(old_dice))

        bonus_status, upper_sum, bonus_points = self.scoreboard.get_upper_sum()

        self.reward += (upper_sum - self.upper_sum) * 0.5

        self.upper_sum = upper_sum

        self.reward += bonus_points

    def dice_strength(self, dice):

        dice_counts = self.dice_to_dice_counts(dice)

        score = 0

        max_count = max(dice_counts)
        score += max_count * 5

        for i, count in enumerate(dice_counts):
            value = i + 1
            score += count * value

        return score

    def dice_to_dice_counts(self, dice):
        return np.bincount(dice, minlength=7)[1:]

    def check_if_game_over(self):
        scoreboard_mask = self.scoreboard.get_scoreboard_mask()
        
        if sum(scoreboard_mask) == len(scoreboard_mask):
            self.done = True
            self.final_score = self.scoreboard.score_game()
            self.reward += self.final_score[0] * 0.5
            self.info = 0
            

        
    def set_prints_on(self):
        self.print = True