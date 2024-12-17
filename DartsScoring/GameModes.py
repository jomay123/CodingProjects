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

    
        

class OneTwoOneGame:
    target = 122
    def __init__(self):
        """Initialize the One-Two-One game mode."""
        self.current_target = 121  # Starting target
        self.turns_taken = 0       # Total turns taken
        self.remaining_attempts = 3  # Attempts per target
        self.game_over = False     # Flag for game completion

    def reset_attempts(self):
        """Reset attempts to 3 for a new target."""
        self.remaining_attempts = 3

    def take_turn(self, score_hit):
        """
        Process a player's turn.
        :param score_hit: The score achieved in the turn.
        """
        if self.game_over:
            print("Game over! No more turns allowed.")
            return

        # Deduct the hit score from the current target
        self.current_target -= score_hit
        self.turns_taken += 3
        self.remaining_attempts -= 1

        # Check if target is completed
        if self.current_target == 0:
            print(f"Target {self.current_target + 1} completed!")
            self.move_to_next_target()
        elif self.remaining_attempts == 0:
            # Out of attempts and target not completed
            print(f"Failed to complete {self.current_target + 1}. Game over!")
            self.game_over = True

    def move_to_next_target(self):
        """Move to the next target score and reset attempts."""
        if self.target > 130:
            print("Congratulations! You have completed all targets!")
            self.game_over = True
        else:
            self.current_target = self.target  # Increment target
            self.target += 1
            self.reset_attempts()  # Reset attempts for new target
            print(f"New target is {self.current_target}.")

    def is_game_over(self):
        """Return whether the game is over."""
        return self.game_over

    def get_game_summary(self):
        """Return a summary of the game."""
        if self.game_over and self.current_target > 130:
            return f"Game Completed! Total Darts Taken: {self.turns_taken}"
        elif self.game_over:
            return f"Game Over! Target Reached: {self.target}, Total Darts: {self.turns_taken}"

  
