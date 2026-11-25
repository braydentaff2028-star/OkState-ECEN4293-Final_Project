import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt 
import numpy as np
from game.GUI import draw_game
from game.game_engine import TetrisGame
from game.tetrominos import Tetromino

def test_draw_game():
  game = TetrisGame()

  fig, ax = draw_game(game)

  assert fig is not None
  assert ax is not None

  plt.close(fig)


def test_active_tetrominos():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 5
  game.current_col = 2

  fig, ax = draw_game(game)
  displayed_board = ax.images[0].get_array()

  assert np.all(displayed_board[5, 2:6] == 1)

  plt.close(fig)


def test_draw_game_doesnt_modify_board():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 5
  game.current_col = 2

  original_board = game.board.copy()

  fig, ax = draw_game(game)

  assert np.array_equal(game.board, original_board)
  plt.close(fig)


def test_game_over_display():
  game = TetrisGame()
  game.is_game_over = True
  game.score = 1800

  fig, ax = draw_game(game)

  assert ax.get_title() == "GAME OVER\nScore: 1800"

  plt.close(fig)


def test_score_display():
  game = TetrisGame()
  game.score = 1200
  game.total_lines_cleared = 6

  fig, ax = draw_game(game)
  assert ax.get_title() == "Score: 1200 | Lines Cleared: 6"

  plt.close(fig)

  
