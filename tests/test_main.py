import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from types import SimpleNamespace
from game.main import handle_keypress
from game.game_engine import TetrisGame
from game.tetrominos import Tetromino

def test_left_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_col = 4

  fig, ax = plt.subplots()
  event = SimpleNamespace(key="left")

  handle_keypress(event, game, ax)
  assert game.current_col == 3
  plt.close(fig)


def test_right_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_col = 3

  fig, ax = plt.subplots()
  event = SimpleNamespace(key="right")

  handle_keypress(event, game, ax)
  assert game.current_col == 4
  plt.close(fig)


def test_down_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0

  fig, ax = plt.subplots()
  event = SimpleNamespace(key="down")

  handle_keypress(event, game, ax)
  assert game.current_row == 1
  plt.close(fig)


def test_x_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(3)

  original_shape = game.active_tetromino.shape()

  fig, ax = plt.subplots()
  event = SimpleNamespace(key = "x")

  handle_keypress(event, game, ax)

  expected_shape = np.rot90(original_shape, k=-1)
  assert np.array_equal(game.active_tetromino.shape, expected_shape)
  plt.close(fig)


def test_z_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(3)

  original_shape = game.active_tetromino.shape()

  fig, ax = plt.subplots()
  event = SimpleNamespace(key = "z")

  handle_keypress(event, game, ax)

  expected_shape = np.rot90(original_shape, k=1)
  assert np.array_equal(game.active_tetromino.shape, expected_shape)
  plt.close(fig)


def test_hard_drop():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0
  game.current_col = 3

  fig, ax = plt.subplots()
  event = SimpleNamespace(key=" ")

  handle_keypress(event, game, ax)
  assert np.all(game.board[19, 3:7] == 1)
  plt.close(fig)
  
