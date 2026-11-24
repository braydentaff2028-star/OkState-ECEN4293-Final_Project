import numpy as np
from game.board import (create_board, is_valid, place_tetromino, line_clear, game_over)

def test_create_board():
  board = create_board()

  assert board.shape == (20, 10)
  assert np.all(board == 0)


def test_valid_position():
  board = create_board()
  piece = np.array([[1, 1], [1,1]])

  assert is_valid(board, piece, 0, 0)


def test_invalid_position():
  board = create_board()
  piece = np.array([[1, 1], [1, 1]])

  assert not is_valid(board, piece, 0, 9)
  assert not is_valid(board, piece, 19, 0)


def test_piece_overlap():
  board = create_board()
  piece = np.array([[1]])

  board[0, 0] = 2

  assert not is_valid(board, piece, 0, 0)


def test_piece_above_board():
  board = create_board()
  piece = np.array([[1, 1]])

  assert is_valid(board, piece, -1, 0)


def test_place_piece():
  board = create_board()
  piece = np.array([[1, 1], [0, 1]])

  place_tetromino(board, piece, 0, 2)

  assert board[0, 2] == 1
  assert board[0, 3] == 1
  assert board[1, 3] == 1


def test_clear_completed_rows():
  board = create_board()
  board[19, :] = 1
  board[0, 0] = 2

  board, rows_cleared = line_clear(board)

  assert rows_cleared == 1
  assert np.all(board[0] == 0)
  assert board[1, 0] == 2


def test_no_completed_rows():
  board = create_board()
  board[19, 0] = 1

  updated_board, rows_cleared = line_clear(board)

  assert rows_cleared == 0
  assert np.array_equal(updated_board, board)


def test_game_over():
  board = create_board()

  assert not game_over(board)

  board[0, 5] = 1

  assert game_over(board)
