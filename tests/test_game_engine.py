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

