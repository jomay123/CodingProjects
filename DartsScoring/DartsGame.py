import tkinter as tk
from tkinter import messagebox
from GameModes import Game
from player import CPUPlayer
from utils import display_scoreboard_ui

class DartsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Darts Scoring App")
        self.root.geometry("600x400")

        self.game = Game()
        self.current_player_index = 0

        # UI Elements
        self.title_label = tk.Label(root, text="Darts Scoring App", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Add Player Section
        self.add_player_frame = tk.Frame(root)
        self.add_player_frame.pack(pady=10)

        tk.Label(self.add_player_frame, text="Player Name:").grid(row=0, column=0, padx=5)
        self.player_name_entry = tk.Entry(self.add_player_frame)
        self.player_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.add_player_frame, text="CPU? (yes/no):").grid(row=1, column=0, padx=5)
        self.is_cpu_entry = tk.Entry(self.add_player_frame)
        self.is_cpu_entry.grid(row=1, column=1, padx=5)

        tk.Label(self.add_player_frame, text="Difficulty (easy/medium/hard):").grid(row=2, column=0, padx=5)
        self.difficulty_entry = tk.Entry(self.add_player_frame)
        self.difficulty_entry.grid(row=2, column=1, padx=5)

        tk.Button(self.add_player_frame, text="Add Player", command=self.add_player).grid(row=3, columnspan=2, pady=10)

        self.players_label = tk.Label(root, text="Players: None", font=("Arial", 12))
        self.players_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game, state=tk.DISABLED)
        self.start_button.pack(pady=10)

    def add_player(self):
        player_name = self.player_name_entry.get().strip()
        is_cpu = self.is_cpu_entry.get().strip().lower() == "yes"
        difficulty = self.difficulty_entry.get().strip().lower()

        if player_name:
            self.game.add_player(player_name, is_cpu=is_cpu, difficulty=difficulty if is_cpu else None)
            self.players_label.config(text=f"Players: {', '.join([p.name for p in self.game.players])}")
            self.player_name_entry.delete(0, tk.END)
            self.is_cpu_entry.delete(0, tk.END)
            self.difficulty_entry.delete(0, tk.END)

            if len(self.game.players) > 1:
                self.start_button.config(state=tk.NORMAL)  # Enable Start button if >1 player
        else:
            messagebox.showwarning("Invalid Input", "Player name cannot be empty.")

    def start_game(self):
        self.add_player_frame.pack_forget()
        self.start_button.pack_forget()

        # Dynamic Player Prompt and Score Input
        self.current_player_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.current_player_label.pack(pady=10)

        self.score_entry = tk.Entry(self.root, font=("Arial", 12))
        self.score_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit Score", command=self.next_turn)
        self.submit_button.pack(pady=10)

        # Scoreboard
        self.scoreboard_frame = tk.Frame(self.root)
        self.scoreboard_frame.pack(pady=20)
        display_scoreboard_ui(self.scoreboard_frame, self.game)

        self.update_prompt()  # Start with the first player

    def update_prompt(self):
     """Update the dynamic text to indicate the current player's turn."""
     current_player = self.game.players[self.current_player_index]
     self.current_player_label.config(text=f"{current_player.name}, enter your score:")

    def next_turn(self):
     """Process the score entered and move to the next player."""
     current_player = self.game.players[self.current_player_index]

    # Initialize score variable
     score = None

     # Handle CPU Turns Automatically
     if isinstance(current_player, CPUPlayer):
        # Automatically take CPU's turn and calculate score
        score = current_player.take_turn(self.game.scores[current_player.name])
       # messagebox.showinfo("CPU Turn", f"{current_player.name} (CPU) scored {score}!")
     else:
        # Process user input for human players
        score_input = self.score_entry.get()
        if not score_input.isdigit() or int(score_input) > 180 or int(score_input) < 0:
            messagebox.showerror("Invalid Score", "Score must be between 0 and 180.")
            return  # Exit early if the input is invalid
        score = int(score_input)

     # Update the score and refresh the scoreboard
     self.game.update_score(current_player.name, score)
     self.score_entry.delete(0, tk.END)  # Clear input for the next turn
     display_scoreboard_ui(self.scoreboard_frame, self.game)

     # Check for Winner
     winner = self.game.get_winner()
     if winner:
        messagebox.showinfo("Game Over", f"Congratulations, {winner} wins!")
        self.root.destroy()
        return

     # Move to the Next Player
     self.current_player_index = self.game.next_player()
     self.update_prompt()

     # **Auto-Advance for CPU Players**
     if isinstance(self.game.players[self.current_player_index], CPUPlayer):
        self.root.after(1500, self.next_turn)  # Automatically trigger the next turn


 

if __name__ == "__main__":
    root = tk.Tk()
    app = DartsApp(root)
    root.mainloop()
