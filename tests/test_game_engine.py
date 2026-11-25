import numpy as np
from game.game_engine import TetrisGame
from game.tetrominos import Tetromino

def test_game_initialize():
  game = TetrisGame()

  assert game.board.shape == (20, 10)
  assert np.all(game.board == 0)
  assert game.total_lines_cleared == 0
  assert not game.is_game_over
  assert game.active_tetromino is not None


def test_tetromino_spawning(monkeypatch):
  monkeypatch.setattr("game.game_engine.random.choice", lambda options: 1)

  game = TetrisGame()

  assert game.active_tetromino.tetromino_id == 1
  assert game.current_row == 0
  assert game.current_col == 3


def test_move_left():
  game = TetrisGame()

  game.active_tetromino = Tetromino(2)
  game.current_row = 0
  game.current_col = 4

  game.move_left()

  assert game.current_col == 3


def test_move_right():
  game = TetrisGame()

  game.active_tetromino = Tetromino(2)
  game.current_row = 0
  game.current_col = 4

  game.move_right()

  assert game.current_col == 5


def test_move_down():
  game = TetrisGame()

  game.active_tetromino = Tetromino(2)
  game.current_row = 0
  game.current_col = 4

  game.board[2, 3] = 9
  game.move_down()

  assert game.current_row == 1
  assert game.current_col == 4


def test_clockwise_rotation():
  game = TetrisGame()
  game.active_tetromino = Tetromino(3)
  original_shape = game.active_tetromino.shape.copy()

  game.rotate_clockwise()

  expected_shape = np.rot90(original_shape, k=-1)

  assert np.array_equal(game.active_tetromino.shape, expected_shape)


def test_lock_tetromino():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 18
  game.current_col = 3

  game.lock_tetromino()

  assert np.all(game.board[18, 3:7] == 1)
  assert game.total_lines_cleared == 0


def test_hard_drop_to_bottom():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0
  game.current_col = 3

  game.hard_drop()

  assert np.all(game.board[19, 3:7] == 1)


def test_hard_drop_to_obstacle():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0
  game.current_col = 3

  game.board[18, 3] = 9

  game.hard_drop()

  assert np.all(game.board[17, 3:7] == 1)
  assert game.board[18, 3] == 9


def test_initial_score():
  game = TetrisGame()
  assert game.score == 0


def test_single_line_score():
  game = TetrisGame()
  game.update_score(1)
  assert game.score == 100


def test_double_line_score():
  game = TetrisGame()
  game.update_score(2)
  assert game.score == 300


def test_triple_line_score():
  game = TetrisGame()
  game.update_score(3)
  assert game.score == 500


def test_quad_line_score():
  game = TetrisGame()
  game.update_score(4)
  assert game.score == 800


def test_score_accumulates():
  game = TetrisGame()
  game.update_score(1)
  game.update_score(2)
  game.update_score(3)
  game.update_score(4)
  assert game.score == 1700


def test_upcoming_tetromino():
  game = TetrisGame()
  assert game.upcoming_tetromino is not None
  assert game.active_tetromino is not None


def test_upcoming_to_active():
  game = TetrisGame()
  upcoming = game.upcoming_tetromino
  game.spawn_tetromino()
  assert game.active_tetromino is upcoming


def test_upcoming_is_selected(monkeypatch):
  game = TetrisGame()
  monkeypatch.setattr("game.game_engine.random.choice", lambda options: 2)

  game.spawn_tetromino()

  assert game.upcoming_tetromino.tetromino_id == 2


def test_initial_level():
    game = TetrisGame()

    assert game.level == 1
    assert game.drop_interval == 500


def test_level_two():
    game = TetrisGame()
    game.total_lines_cleared = 10

    game.update_level()

    assert game.level == 2
    assert game.drop_interval == 450


def test_level_three():
    game = TetrisGame()
    game.total_lines_cleared = 20

    game.update_level()

    assert game.level == 3
    assert game.drop_interval == 400


def test_maximum_drop_speed():
    game = TetrisGame()
    game.total_lines_cleared = 80

    game.update_level()

    assert game.level == 9
    assert game.drop_interval == 100


def test_drop_speed_does_not_exceed_maximum():
    game = TetrisGame()
    game.total_lines_cleared = 100

    game.update_level()

    assert game.level == 11
    assert game.drop_interval == 100

