import tkinter as tk
def display_scoreboard_ui(frame, game):
    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    players = list(game.scores.items())

    # Grid Layout for Two Players
    for idx, (player, score) in enumerate(players):
        # Player Name
        name_label = tk.Label(frame, text=player, font=("Arial", 16, "bold"))
        name_label.grid(row=0, column=idx, padx=50, pady=5)

        # Current Score
        score_label = tk.Label(frame, text=f"Score: {score}", font=("Arial", 24, "bold"))
        score_label.grid(row=1, column=idx, padx=50, pady=5)

        # Last 5 Scores
        last_scores = game.get_last_n_scores(player, n=5)
        last_scores_text = ", ".join(map(str, last_scores)) if last_scores else "No scores yet"
        last_scores_label = tk.Label(frame, text=f"Last 5: {last_scores_text}", font=("Arial", 12))
        last_scores_label.grid(row=2, column=idx, padx=50, pady=5)

        # Total Turns
        total_turns = len(game.score_history[player])
        turns_label = tk.Label(frame, text=f"Turns: {total_turns}", font=("Arial", 12))
        turns_label.grid(row=3, column=idx, padx=50, pady=5)

