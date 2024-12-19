import random

class Player:
    def __init__(self, name, starting_score):
        self.name = name
        self.score = starting_score
        self.game_wins = 0

class CPUPlayer(Player):
    def __init__(self, name, difficulty, starting_score):
        super().__init__(name, starting_score)
        self.difficulty = difficulty

    def take_turn(self, remaining_score):
        if self.difficulty == "easy":
            return random.randint(1, 20)
        elif self.difficulty == "medium":
            return min(remaining_score, random.randint(10, 50))
        elif self.difficulty == "hard":
            if remaining_score <= 50:
                return remaining_score
            return min(remaining_score, random.randint(40, 60))
        return 0
