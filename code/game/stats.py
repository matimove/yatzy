class Stats:
    def __init__(self):
        self.scores = []
        self.bonus_achieved = []

    def add_score(self, score):
        self.scores.append(score[0])
        self.bonus_achieved.append(score[1])
        
    def show_stats(self):
        dct = {}
        avg = sum(self.scores)/len(self.scores)

        highest = max(self.scores)

        dct["Games played"] = len(self.scores)
        dct["Average"] = avg
        dct["Highest score"] = highest

        return dct