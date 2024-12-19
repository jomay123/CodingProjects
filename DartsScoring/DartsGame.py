import tkinter as tk
from tkinter import messagebox
from GameModes import Game, OneTwoOneGame  # Import both game modes
from player import CPUPlayer, Player
from utils import display_scoreboard_ui
from time import sleep


class DartsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Darts Scoring App")
        self.root.geometry("1000x1000")

        self.game = None  # Placeholder for the game instance
        self.current_player_index = 0
        self.selected_mode = None  # Track the selected game mode

        # Title Label
        self.title_label = tk.Label(root, text="Darts Scoring App", font=("Arial", 16))
        self.title_label.pack(pady=10)

        # Mode Selection
        self.mode_frame = tk.Frame(root)
        self.mode_frame.pack(pady=20)

        tk.Label(self.mode_frame, text="Select Game Mode:", font=("Arial", 12)).pack()

        # Radio buttons to select game mode
        self.mode_var = tk.StringVar(value="standard")  # Default to standard
        tk.Radiobutton(self.mode_frame, text="Standard Game", variable=self.mode_var, value="standard").pack()
        tk.Radiobutton(self.mode_frame, text="One-Two-One", variable=self.mode_var, value="onetwoone").pack()

        # Start button
        self.start_button = tk.Button(root, text="Start Game", command=self.initialize_game)
        self.start_button.pack(pady=10)

    def initialize_game(self):
        """Initialize the selected game mode."""
        self.selected_mode = self.mode_var.get()

        if self.selected_mode == "standard":
            self.setup_player_add_screen()
        elif self.selected_mode == "onetwoone":
            self.game = OneTwoOneGame()
            self.start_game()

    def setup_player_add_screen(self):
        """Setup the screen to add players for the standard game."""
        self.mode_frame.pack_forget()
        self.start_button.pack_forget()

        self.game = Game()

        # Add Player UI
        self.add_player_frame = tk.Frame(self.root)
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

        self.slider_label = tk.Label(root, text="Game Counter:", font=("Arial", 14))
        self.slider_label.pack(pady=5)

        self.game_counter_slider = tk.Scale(
            root,
            from_=1,  # Minimum value
            to=30,  # Maximum value
            orient="horizontal",  # Horizontal slider
            length=300,
            command=self.update_game_counter
        )
        self.game_counter_slider.pack(pady=5)

        # Display the current value of the game counter
        self.game_counter_value = tk.Label(root, text="Counter Value: 0", font=("Arial", 12))
        self.game_counter_value.pack(pady=5)


        tk.Button(self.add_player_frame, text="Add Player", command=self.add_player).grid(row=3, columnspan=2, pady=10)

        self.players_label = tk.Label(self.root, text="Players: None", font=("Arial", 12))
        self.players_label.pack(pady=10)

        self.start_game_button = tk.Button(self.root, text="Start Game", command=self.start_game, state=tk.DISABLED)
        self.start_game_button.pack(pady=10)

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
                self.start_game_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("Invalid Input", "Player name cannot be empty.")

    def start_game(self):
        """Set up the main game UI."""
        if self.selected_mode == "standard":
            self.add_player_frame.pack_forget()
            self.start_game_button.pack_forget()

        # Main UI elements
        self.current_player_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.current_player_label.pack(pady=10)

        self.score_entry = tk.Entry(self.root, font=("Arial", 12))
        self.score_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit Score", command=self.next_turn)
        self.submit_button.pack(pady=10)

        self.scoreboard_frame = tk.Frame(self.root)
        self.scoreboard_frame.pack(pady=20)

        display_scoreboard_ui(self.scoreboard_frame, self.game)
        self.update_prompt()

    def update_prompt(self):
     """Update the UI prompt dynamically."""
     # Ensure the window is still valid before updating
     if not self.root.winfo_exists():
        return

     if self.selected_mode == "onetwoone":
        self.current_player_label.config(
            text=f"Target: {self.game.current_target}, Attempts Left: {self.game.remaining_attempts}"
        )
     else:
        current_player = self.game.players[self.current_player_index]
        self.current_player_label.config(text=f"{current_player.name}, enter your score:")


    def update_game_counter(self, value):
        """Update the game counter when the slider changes."""
        if self.game:  # Ensure the game exists
            self.game.game_counter = int(value)
        self.game_counter_value.config(text=f"Counter Value: {value}")

    def next_turn(self):
     """Handle the logic for both game modes."""
     if self.selected_mode == "onetwoone":
        score_input = self.score_entry.get()
        if not score_input.isdigit():
            messagebox.showerror("Invalid Input", "Enter a valid score.")
            return
        if int(score_input) > self.game.current_target:
            messagebox.showerror("Invalid Input", "Enter a valid score.")
            return
        self.game.take_turn(int(score_input))
        display_scoreboard_ui(self.scoreboard_frame, self.game)

        if self.game.is_game_over():
            messagebox.showinfo("Game Over", self.game.get_game_summary())
            self.root.destroy()
        self.update_prompt()
     else:
        current_player = self.game.players[self.current_player_index]
        score_input = self.score_entry.get()
        if not score_input.isdigit():
            return
        score = int(score_input)
        if score > 180:
            messagebox.showerror("Invalid Score", "Score must be between 0 and 180.")
            return
        self.game.update_score(current_player.name, score)
        display_scoreboard_ui(self.scoreboard_frame, self.game)

        # Check if the current player has won the game
        if self.game.scores[current_player.name] == 0:
            # Track total games played
            winner = self.game.get_winner()
            if not hasattr(self, "games_played"):
                self.games_played = 0  # Initialize games played counter

            self.games_played += 1

            if self.games_played < self.game_counter_slider.get():
                # Reset scores and start a new game
                messagebox.showinfo("Game Over", f"Congratulations, {current_player.name} wins this game!")
                self.reset_game()
                return
            else:
                # End the program after all games have been played
                messagebox.showinfo("Game Over", f"Congratulations, {current_player.name} wins the final game!")
                sleep(5)
                self.root.destroy()
                return

        # Move to the next player
        self.current_player_index = self.game.next_player()
        self.update_prompt()


    def reset_game(self):
     """Reset the game state for the next match in Standard Game mode."""
     for player in self.game.players:
        self.game.scores[player.name] = 501  # Reset scores to 501
        self.game.score_history[player.name] = []
     self.current_player_index = 0  # Start with the first player
     display_scoreboard_ui(self.scoreboard_frame, self.game)
     self.update_prompt()




if __name__ == "__main__":
    root = tk.Tk()
    app = DartsApp(root)
    root.mainloop()
