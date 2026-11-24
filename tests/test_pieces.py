import numpy as np
from game.tetrominos import TETROMINOS, Tetromino

def test_all_tetrominos_exsist():
  assert len(TETROMINOS) == 7

  for tetromino_id in range(1, 8):
    assert tetromino_id in TETROMINOS


def test_each_tetromino_has_four_cells():
  for tetromino in TETROMINOS.values():
    assert np.count_nonzero(tetromino) == 4


def test_tetromino_creation():
  for tetromino_id in range(1, 8):
    tetromino = Tetromino(tetromino_id)

    assert tetromino.tetromino_id == tetromino_id
    assert np.array_equal(tetromino.shape, TETROMINOS[tetromino_id])


def test_clockwise_rotation():
  tetromino = Tetromino(1)

  original_shape = tetromino.shape.copy()
  tetromino.rotate_clockwise()
  expected_shape = np.rot90(original_shape, k=-1)

  assert np.array_equal(tetromino.shape, expected_shape)


def test_counterclockwise_rotation():
  tetromino = Tetromino(1)
  original_shape = tetromino.shape.copy()
  tetromino.rotate_counterclockwise()
  expected_shape = np.rot90(original_shape, k=1)

  assert np.array_equal(tetromino.shape, expected_shape)


def test_four_clockwise_rotations():
  tetromino = Tetromino(3)
  original_shape = tetromino.shape.copy()

  for _ in range(4):
    tetromino.rotate_clockwise()

  assert np.array_equal(tetromino.shape, original_shape)


def test_rotation_doesnt_change_og():
  original_shape = TETROMINOS[1].copy()

  tetromino = Tetromino(1)
  tetromino.rotate_clockwise()

  assert np.array_equal(TETROMINOS[1], original_shape)
