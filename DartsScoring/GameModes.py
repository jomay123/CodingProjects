from player import Player, CPUPlayer

class Game:
    def __init__(self, starting_score=501):
        self.starting_score = starting_score
        self.scores = {}
        self.players = []
        self.score_history = {}
        self.current_player_index = 0

    def add_player(self, player_name, is_cpu=False, difficulty="medium"):
        if is_cpu:
            player = CPUPlayer(player_name, difficulty, self.starting_score)
        else:
            player = Player(player_name, self.starting_score)
        self.players.append(player)
        self.scores[player_name] = self.starting_score
        self.score_history[player_name] = []

    def update_score(self, player_name, score):
        if score is None:
            return
        current_score = self.scores[player_name]
        if current_score - score >= 0:
            self.scores[player_name] -= score
            self.score_history[player_name].append(score)
        elif score > 180:
            print(f"Score Must be below 180 please enter again")
        else:
            print(f"{player_name} bust! Score remains: {current_score}")

    def get_winner(self):
        for player_name, score in self.scores.items():
            if score == 0:
                return player_name
        return None

    def next_player(self):
        print(self.current_player_index, "Next player function")
        if self.current_player_index == (len(self.players) - 1):
            self.current_player_index = 0
        else:
            self.current_player_index += 1
        return self.current_player_index
     
    def get_last_n_scores(self, player_name, n=5):
     """Return the last n scores for a given player."""
     return self.score_history[player_name][-n:] if player_name in self.score_history else []

    
        
