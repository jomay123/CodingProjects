import random

class Game:
    def __init__(self, starting_score=501):
        self.starting_score = starting_score
        self.scores = {}
        self.players = []
        self.current_player_index = 0

    def add_player(self, player_name, is_cpu=False, difficulty="medium"):
        if is_cpu:
            player = CPUPlayer(player_name, difficulty, self.starting_score)
        else:
            player = Player(player_name, self.starting_score)
        self.players.append(player)
        self.scores[player_name] = self.starting_score

    def update_score(self, player_name, score):
        current_score = self.scores[player_name]
        if current_score - score >= 0:
            self.scores[player_name] -= score
        else:
            print(f"{player_name} bust! Score remains: {current_score}")

    def get_winner(self):
        for player_name, score in self.scores.items():
            if score == 0:
                return player_name
        return None

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

class Player:
    def __init__(self, name, starting_score):
        self.name = name
        self.score = starting_score

class CPUPlayer(Player):
    def __init__(self, name, difficulty, starting_score):
        super().__init__(name, starting_score)
        self.difficulty = difficulty

    def take_turn(self, remaining_score):
        if self.difficulty == "easy":
            return random.randint(1, 20)  # Random lower scores
        elif self.difficulty == "medium":
            return min(remaining_score, random.randint(10, 50))  # Aim for decent scores
        elif self.difficulty == "hard":
            # Aim for the exact score to finish or the highest valid score
            if remaining_score <= 50:
                return remaining_score  # Finish the game
            return min(remaining_score, random.randint(40, 60))  # High scores
        return 0  # Fallback

def main():
    game = Game()
    num_players = int(input("Enter number of players (including CPUs): "))

    for i in range(num_players):
        name = input(f"Enter name for Player {i + 1}: ")
        is_cpu = input("Is this player a CPU? (yes/no): ").strip().lower() == "yes"

        if is_cpu:
            difficulty = input("Select difficulty for CPU (easy/medium/hard): ").strip().lower()
            game.add_player(name, is_cpu=True, difficulty=difficulty)
        else:
            game.add_player(name)

    print("Game starting!")
    while True:
        player = game.players[game.current_player_index]
        if isinstance(player, CPUPlayer):
            score = player.take_turn(game.scores[player.name])
            print(f"{player.name} (CPU) scored {score}!")
        else:
            print(f"{player.name}'s turn. Current score: {game.scores[player.name]}")
            score = int(input("Enter score: "))

        game.update_score(player.name, score)

        winner = game.get_winner()
        if winner:
            print(f"Congratulations, {winner} wins!")
            break

        game.next_player()

if __name__ == "__main__":
    main()
