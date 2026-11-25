#Simulation Runner
import csv
import random
import os
from game.game_engine import TetrisGame
from game.automation import (play_random_move, play_hole_minimization_move, play_height_minimization_move, play_combined_move, calculate_board_height, count_holes)

# Number of games per configuration
GAMES_PER_CONFIGURATION = 1000
RANDOM_SEED = 42

# All simulation configurations
CONFIGURATIONS = [
    {"name": "Random", "strategy": "random"},
    {"name": "Minimize Holes", "strategy": "holes"},
    {"name": "Minimize Height", "strategy": "height"},
    {"name": "Combined 70-30", "strategy": "combined", "hole_weight": 0.7, "height_weight": 0.3},
    {"name": "Combined 60-40", "strategy": "combined", "hole_weight": 0.6, "height_weight": 0.4},
    {"name": "Combined 50-50", "strategy": "combined", "hole_weight": 0.5, "height_weight": 0.5},
    {"name": "Combined 40-60", "strategy": "combined", "hole_weight": 0.4, "height_weight": 0.6},
    {"name": "Combined 30-70", "strategy": "combined", "hole_weight": 0.3, "height_weight": 0.7}
]


def run_game(configuration):
    game = TetrisGame()

    maximum_height = calculate_board_height(game.board)

    while not game.is_game_over:

        strategy = configuration["strategy"]

        if strategy == "random":
            play_random_move(game)

        elif strategy == "holes":
            play_hole_minimization_move(game)

        elif strategy == "height":
            play_height_minimization_move(game)

        elif strategy == "combined":
            play_combined_move(
                game,
                configuration["hole_weight"],
                configuration["height_weight"]
            )

        current_height = calculate_board_height(game.board)
        maximum_height = max(maximum_height, current_height)

    return {
        "score": game.score,
        "lines_cleared": game.total_lines_cleared,
        "maximum_height": maximum_height,
        "holes": count_holes(game.board)
    }


def run_simulations():
    random.seed(RANDOM_SEED)
    results_folder = os.path.join("experiments", "results")
    os.makedirs(results_folder, exist_ok=True)

    output_file = os.path.join(results_folder, "simulation_results.csv")

    total_games = len(CONFIGURATIONS) * GAMES_PER_CONFIGURATION
    completed_games = 0

    with open(output_file, "w", newline="") as csvfile:

        fieldnames = [
            "configuration",
            "game_number",
            "hole_weight",
            "height_weight",
            "score",
            "lines_cleared",
            "maximum_height",
            "holes"
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for configuration in CONFIGURATIONS:

            print(f"\nRunning: {configuration['name']}")

            for game_number in range(1, GAMES_PER_CONFIGURATION + 1):

                results = run_game(configuration)

                writer.writerow({
                    "configuration": configuration["name"],
                    "game_number": game_number,
                    "hole_weight": configuration.get("hole_weight", ""),
                    "height_weight": configuration.get("height_weight", ""),
                    **results
                })

                completed_games += 1

                if game_number % 100 == 0:
                    print(
                        f"{game_number}/{GAMES_PER_CONFIGURATION} games completed "
                        f"for {configuration['name']}"
                    )

            print(f"Completed {configuration['name']}")

    print(f"\nAll {total_games} simulations completed!")
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    run_simulations()
