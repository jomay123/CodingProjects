import tkinter as tk
def display_scoreboard_ui(frame, game):
    # Clear the existing widgets in the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Check if it's a One-Two-One game
    if hasattr(game, "current_target") and hasattr(game, "remaining_attempts"):
        # One-Two-One Game Mode UI
        target_label = tk.Label(frame, text=f"Target: {game.current_target}", font=("Arial", 24, "bold"))
        target_label.grid(row=0, column=0, padx=20, pady=10)

        attempts_label = tk.Label(frame, text=f"Attempts Left: {game.remaining_attempts}", font=("Arial", 16))
        attempts_label.grid(row=1, column=0, padx=20, pady=5)

        turns_label = tk.Label(frame, text=f"Total Turns: {game.turns_taken}", font=("Arial", 16))
        turns_label.grid(row=2, column=0, padx=20, pady=5)

    else:
        # Standard Game Mode UI
        players = list(game.scores.items())

        # Set up grid layout for multiple players
        for idx, (player_name, score) in enumerate(players):
            col = idx  # Column index for layout

            # Player Name
            name_label = tk.Label(frame, text=player_name, font=("Arial", 16, "bold"))
            name_label.grid(row=0, column=col, padx=50, pady=5)

            # Current Score
            score_label = tk.Label(frame, text=f"Score: {score}", font=("Arial", 24, "bold"))
            score_label.grid(row=1, column=col, padx=50, pady=5)

            # Last 5 Scores
            if hasattr(game, "get_last_n_scores") and hasattr(game, "score_history"):
                last_scores = game.get_last_n_scores(player_name, n=5)
                last_scores_text = ", ".join(map(str, last_scores)) if last_scores else "No scores yet"
                last_scores_label = tk.Label(frame, text=f"Last 5: {last_scores_text}", font=("Arial", 12))
                last_scores_label.grid(row=2, column=col, padx=50, pady=5)

                # Total Turns
                total_turns = len(game.score_history[player_name]) * 3
                turns_label = tk.Label(frame, text=f"Darts: {total_turns}", font=("Arial", 12))
                turns_label.grid(row=3, column=col, padx=50, pady=5)

