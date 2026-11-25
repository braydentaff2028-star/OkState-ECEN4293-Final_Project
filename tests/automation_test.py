import numpy as np
import pytest

from game.automation import (
    get_unique_rotations,
    get_all_legal_placements,
    get_random_placement,
    execute_placement,
    play_random_move,
    count_holes,
    evaluate_holes,
    get_best_hole_placement,
    play_hole_minimization_move,
    calculate_board_height,
    evaluate_height,
    get_best_height_placement,
    play_height_minimization_move,
    evaluate_combined,
    get_best_combined_placement,
    play_combined_move,
)

from game.game_engine import TetrisGame
from game.tetrominos import Tetromino
from game.board import is_valid, ROWS, COLS

def test_unique_rotations_for_i_tetromino():
    tetromino = Tetromino(1)

    rotations = get_unique_rotations(tetromino)

    assert len(rotations) == 2


def test_unique_rotations_do_not_modify_original():
    tetromino = Tetromino(1)
    original_shape = tetromino.shape.copy()

    get_unique_rotations(tetromino)

    assert np.array_equal(tetromino.shape, original_shape)
  

def test_legal_placements_are_generated():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)

    assert len(placements) > 0


def test_all_generated_placements_are_legal():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)

    for placement in placements:
        assert is_valid(
            game.board,
            placement["rotation"],
            placement["row"],
            placement["col"]
        )


def test_placements_are_at_the_bottommost_available_position():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)

    for placement in placements:
        assert not is_valid(
            game.board,
            placement["rotation"],
            placement["row"] + 1,
            placement["col"]
        )


def test_no_placements_when_spawn_area_is_blocked():
    game = TetrisGame()
    game.board[0, :] = 1

    placements = get_all_legal_placements(game)

    assert placements == []


def test_random_placement_returns_legal_placement():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)
    placement = get_random_placement(game)

    assert any(
        placement["row"] == option["row"]
        and placement["col"] == option["col"]
        and np.array_equal(
            placement["rotation"],
            option["rotation"]
        )
        for option in placements
    )


def test_random_placement_returns_none_when_no_placements():
    game = TetrisGame()
    game.board[0, :] = 1

    placement = get_random_placement(game)

    assert placement is None


def test_execute_placement_locks_tetromino():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placement = get_all_legal_placements(game)[0]

    execute_placement(game, placement)

    assert np.count_nonzero(game.board) >= 4


def test_execute_placement_with_none_causes_game_over():
    game = TetrisGame()

    execute_placement(game, None)

    assert game.is_game_over


def test_count_holes_on_empty_board():
    board = np.zeros((ROWS, COLS), dtype=int)

    assert count_holes(board) == 0


def test_count_holes_detects_empty_space_below_blocks():
    board = np.zeros((ROWS, COLS), dtype=int)

    board[6:, 0] = 1
    board[7, 0] = 0

    assert count_holes(board) == 1


def test_evaluate_holes_does_not_modify_original_board():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placement = get_all_legal_placements(game)[0]
    original_board = game.board.copy()

    evaluate_holes(game, placement)

    assert np.array_equal(game.board, original_board)


def test_best_hole_placement_minimizes_holes():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)
    best_placement = get_best_hole_placement(game)

    lowest_holes = min(
        evaluate_holes(game, placement)
        for placement in placements
    )

    assert evaluate_holes(game, best_placement) == lowest_holes


def test_empty_board_has_zero_height():
    board = np.zeros((ROWS, COLS), dtype=int)

    assert calculate_board_height(board) == 0


def test_board_height_is_calculated_correctly():
    board = np.zeros((ROWS, COLS), dtype=int)
    board[15, 3] = 1

    assert calculate_board_height(board) == 5


def test_evaluate_height_does_not_modify_original_board():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placement = get_all_legal_placements(game)[0]
    original_board = game.board.copy()

    evaluate_height(game, placement)

    assert np.array_equal(game.board, original_board)


def test_best_height_placement_minimizes_height():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)
    best_placement = get_best_height_placement(game)

    lowest_height = min(
        evaluate_height(game, placement)
        for placement in placements
    )

    assert evaluate_height(game, best_placement) == lowest_height


def test_hole_evaluation_accounts_for_cleared_lines():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    game.board[ROWS - 1, 4:] = 1

    placement = {
        "rotation": game.active_tetromino.shape,
        "row": ROWS - 1,
        "col": 0
    }

    assert evaluate_holes(game, placement) == 0


def test_height_evaluation_accounts_for_cleared_lines():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    game.board[ROWS - 1, 4:] = 1

    placement = {
        "rotation": game.active_tetromino.shape,
        "row": ROWS - 1,
        "col": 0
    }

    assert evaluate_height(game, placement) == 0


def test_combined_evaluation_returns_numeric_score():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placement = get_all_legal_placements(game)[0]

    score = evaluate_combined(game, placement)

    assert isinstance(score, (int, float))


def test_combined_evaluation_uses_configurable_weights():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placement = get_all_legal_placements(game)[0]

    holes = evaluate_holes(game, placement)
    height = evaluate_height(game, placement)

    expected_score = (
        0.5 * (holes / (ROWS * COLS))
        + 0.5 * (height / ROWS)
    )

    score = evaluate_combined(
        game,
        placement,
        hole_weight=0.5,
        height_weight=0.5
    )

    assert score == pytest.approx(expected_score)


def test_best_combined_placement_minimizes_score():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    placements = get_all_legal_placements(game)
    best_placement = get_best_combined_placement(game)

    lowest_score = min(
        evaluate_combined(game, placement)
        for placement in placements
    )

    assert evaluate_combined(game, best_placement) == pytest.approx(
        lowest_score
    )


@pytest.mark.parametrize(
    "play_function",
    [
        play_random_move,
        play_hole_minimization_move,
        play_height_minimization_move,
        play_combined_move
    ]
)
def test_ai_strategy_executes_a_move(play_function):
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    play_function(game)

    assert np.count_nonzero(game.board) >= 4


@pytest.mark.parametrize(
    "play_function",
    [
        play_random_move,
        play_hole_minimization_move,
        play_height_minimization_move,
        play_combined_move
    ]
)
def test_ai_strategy_handles_no_legal_placements(play_function):
    game = TetrisGame()
    game.board[0, :] = 1

    play_function(game)

    assert game.is_game_over
