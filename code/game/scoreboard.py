class Scoreboard:
    def __init__(self):
        self.scoreboard = None
    
    def initialize(self):
        self.scoreboard = {"Ones": None,
                           "Twos": None,
                           "Threes": None,
                           "Fours": None,
                           "Fives": None,
                           "Sixes": None,
                           "One Pair": None,
                           "Two Pair": None,
                           "Three of a Kind": None,
                           "Four of a Kind": None,
                           "Small Straight": None,
                           "Large Straight": None,
                           "Full House": None,
                           "Chance": None,
                           "Yatzy": None,
                           }
        self.categories = [
                            "Ones",
                            "Twos",
                            "Threes",
                            "Fours",
                            "Fives",
                            "Sixes",
                            "One Pair",
                            "Two Pair",
                            "Three of a Kind",
                            "Four of a Kind",
                            "Small Straight",
                            "Large Straight",
                            "Full House",
                            "Chance",
                            "Yatzy"
                            ]
        self.bonus_achieved=False
    
    def return_scoreboard(self):
        return self.scoreboard
    
    def get_upper_sum(self):

        upper_section = [self.scoreboard["Ones"],
                    self.scoreboard["Twos"],
                    self.scoreboard["Threes"],
                    self.scoreboard["Fours"],
                    self.scoreboard["Fives"],
                    self.scoreboard["Sixes"]
                    ]
    
        upper_sum = sum(score if score is not None else 0 for score in upper_section)
        
        complete = True

        for item in upper_section:
            if item is None:
                complete = False

        bonus_score = 0

        if complete and upper_sum >= 63 and not self.bonus_achieved:
            print("BONUS ACHIEVED!")
            self.bonus_achieved = True
            bonus_score += 100

        return (complete, upper_sum, bonus_score)
    
    def score_game(self):
    
        top_section_score = sum([
            self.scoreboard["Ones"],
            self.scoreboard["Twos"], 
            self.scoreboard["Threes"], 
            self.scoreboard["Fours"], 
            self.scoreboard["Fives"], 
            self.scoreboard["Sixes"]
            ])
        
        if top_section_score >= 63:
            bonus = 50
        else:
            bonus = 0
        
        total_score = (sum(list(self.scoreboard.values())) + bonus, bonus == 50)

        return total_score
    
    def get_scoreboard_mask(self):
        return [0 if item is None else 1 for item in self.scoreboard.values()]
    
    def place_score(self, dice, placement):
        category_name = self.categories[placement-1]
        
        self.scoreboard[category_name] = self.score_dice(dice.display(), category_name)
        return self.score_dice(dice.display(), category_name)
        

           
    def count_dice(self, dice):
        dct = {}
        for d in dice:
            if d in dct:
                dct[d] += 1
            else:
                dct[d] = 1
        return dct
    

    def score_dice(self, dice, pick):
        
        if pick == 'Ones':
            return dice.count(1)*1
        
        if pick =='Twos':
            return dice.count(2)*2
        
        if pick =='Threes':
            return dice.count(3)*3
        
        if pick =='Fours':
            return dice.count(4)*4
        
        if pick =='Fives':
            return dice.count(5)*5
        
        if pick =='Sixes':
            return dice.count(6)*6
        
        if pick =='One Pair':
            dct = self.count_dice(dice)
            highest_die = 0
            for d in dct:
                if dct[d] >= 2:
                    if d > highest_die:
                        highest_die = d
            return 2*highest_die
        
        if pick =='Two Pair':
            dct = self.count_dice(dice)
            first_pair = 0
            second_pair = 0
            
            for d in dct:
                if dct[d] >= 2:
                    if d > first_pair:
                        second_pair = first_pair
                        first_pair = d
            
            return 2*first_pair + 2*second_pair if first_pair != 0 and second_pair != 0 else 0
        
        if pick =='Three of a Kind':
            dct = self.count_dice(dice)
            for d in dice:
                if dct[d] == 3:
                    return 3*d
            return 0 
        
        if pick =='Four of a Kind':
            dct = self.count_dice(dice)
            for d in dice:
                if dct[d] == 4:
                    return 4*d
            return 0 
        
        if pick =='Small Straight':
            return 15 if dice == [1,2,3,4,5] else 0
        
        if pick =='Large Straight':
            return 20 if dice == [2,3,4,5,6] else 0
        
        if pick =='Full House':
            dct = self.count_dice(dice)
            if dct[dice[0]] in [2,3] and dct[dice[-1]] in [2,3]:
                if len(dct) == 2:
                    return dice[0]*dct[dice[0]] + dice[-1]*dct[dice[-1]]
            return 0
                
        if pick =='Chance':
            return sum(dice)
        
        if pick =='Yatzy':
            return 50 if len(set(dice)) == 1 else 0