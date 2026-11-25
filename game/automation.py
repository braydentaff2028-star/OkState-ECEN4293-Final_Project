import numpy as np
import random
from game.board import is_valid, ROWS, COLS

#Hole VS. Height Weight
HOLE_WEIGHT = 0.7
HEIGHT_WEIGHT = 0.3


def get_unique_rotations(tetromino):
    rotations = []

    for rotation in range(4):
        rotated_shape = np.rot90(tetromino.shape, k=-rotation)

        if not any(np.array_equal(rotated_shape, existing) for existing in rotations):
            rotations.append(rotated_shape)

    return rotations


def get_all_legal_placements(game):
    placements = []

    rotations = get_unique_rotations(game.active_tetromino)

    for rotation in rotations:
        for col in range(COLS - rotation.shape[1] + 1):

            row = 0

            if not is_valid(game.board, rotation, row, col):
                continue

            while is_valid(game.board, rotation, row + 1, col):
                row += 1

            placements.append({
                "rotation": rotation,
                "row": row,
                "col": col
            })

    return placements

def get_random_placement(game):
    placements = get_all_legal_placements(game)

    if not placements:
        return None

    return random.choice(placements)


def execute_placement(game, placement):
    if placement is None:
        game.is_game_over = True
        return

    game.active_tetromino.shape = placement["rotation"]
    game.current_row = placement["row"]
    game.current_col = placement["col"]

    game.lock_tetromino()


def play_random_move(game):
    placement = get_random_placement(game)
    execute_placement(game, placement)


#AI NO. 2 (Minimize Holes)
def count_holes(board):
    holes = 0

    for col in range(COLS):
        block_found = False

        for row in range(ROWS):
            if board[row, col] != 0:
                block_found = True
            elif block_found:
                holes += 1

    return holes


def evaluate_holes(game, placement):
    simulated_board = game.board.copy()

    rotation = placement["rotation"]
    row = placement["row"]
    col = placement["col"]

    for r in range(rotation.shape[0]):
        for c in range(rotation.shape[1]):
            if rotation[r, c] != 0:
                simulated_board[row + r, col + c] = rotation[r, c]

    full_rows = np.all(simulated_board != 0, axis=1)
    lines_cleared = np.count_nonzero(full_rows)

    if lines_cleared > 0:
        remaining_rows = simulated_board[~full_rows]

        empty_rows = np.zeros(
            (lines_cleared, COLS),
            dtype=simulated_board.dtype
        )

        simulated_board = np.vstack((empty_rows, remaining_rows))

    return count_holes(simulated_board)

def get_best_hole_placement(game):
    placements = get_all_legal_placements(game)

    if not placements:
        return None

    best_placement = None
    fewest_holes = float("inf")

    for placement in placements:
        holes = evaluate_holes(game, placement)

        if holes < fewest_holes:
            fewest_holes = holes
            best_placement = placement

    return best_placement


def play_hole_minimization_move(game):
    placement = get_best_hole_placement(game)
    execute_placement(game, placement)


#Ai No. 3 (Minimize Height)
def calculate_board_height(board):
    for row in range(ROWS):
        if np.any(board[row] != 0):
            return ROWS - row

    return 0


def evaluate_height(game, placement):
    simulated_board = game.board.copy()

    rotation = placement["rotation"]
    row = placement["row"]
    col = placement["col"]

    for r in range(rotation.shape[0]):
        for c in range(rotation.shape[1]):
            if rotation[r, c] != 0:
                simulated_board[row + r, col + c] = rotation[r, c]

    full_rows = np.all(simulated_board != 0, axis=1)
    lines_cleared = np.count_nonzero(full_rows)

    if lines_cleared > 0:
        remaining_rows = simulated_board[~full_rows]

        empty_rows = np.zeros(
            (lines_cleared, COLS),
            dtype=simulated_board.dtype
        )

        simulated_board = np.vstack((empty_rows, remaining_rows))

    return calculate_board_height(simulated_board)


def get_best_height_placement(game):
    placements = get_all_legal_placements(game)

    if not placements:
        return None

    best_placement = None
    lowest_height = float("inf")

    for placement in placements:
        height = evaluate_height(game, placement)

        if height < lowest_height:
            lowest_height = height
            best_placement = placement

    return best_placement


def play_height_minimization_move(game):
    placement = get_best_height_placement(game)
    execute_placement(game, placement)


#AI NO.4 ("Optimized")
def evaluate_combined(game, placement, hole_weight=HOLE_WEIGHT, height_weight=HEIGHT_WEIGHT):
    holes = evaluate_holes(game, placement)
    height = evaluate_height(game, placement)

    normalized_holes = holes / (ROWS * COLS)
    normalized_height = height / ROWS

    combined_score = (
        hole_weight * normalized_holes
        + height_weight * normalized_height
    )

    return combined_score


def get_best_combined_placement(game, hole_weight=HOLE_WEIGHT, height_weight=HEIGHT_WEIGHT):
    placements = get_all_legal_placements(game)

    if not placements:
        return None

    best_score = float("inf")
    best_placements = []

    for placement in placements:
        score = evaluate_combined(
            game,
            placement,
            hole_weight,
            height_weight
        )

        if score < best_score:
            best_score = score
            best_placements = [placement]

        elif score == best_score:
            best_placements.append(placement)

    return random.choice(best_placements)


def play_combined_move(game, hole_weight=HOLE_WEIGHT, height_weight=HEIGHT_WEIGHT):
    placement = get_best_combined_placement(
        game,
        hole_weight,
        height_weight
    )

    execute_placement(game, placement)
