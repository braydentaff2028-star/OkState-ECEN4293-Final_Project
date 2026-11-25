import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

TETROMINO_COLORS = [
  "black",
  "cyan",
  "yellow",
  "purple",
  "green",
  "red",
  "blue",
  "orange"
]


def draw_next_tetromino(game, ax):
  ax.clear()

  tetromino = game.upcoming_tetromino.shape

  color_map = ListedColormap(TETROMINOS_COLORS)

  ax.imshow(tetromino, cmap=color_map, vmin=0, vmax=7)

  ax.set_title("NEXT", fontsize=14)

  ax.set_xticks([])
  ax.set_yticks([])

  ax.set_aspect("equal")


def draw_game(game, ax=None):
  if ax is None:
    fig, (ax, preview_ax) = plt.subplots(1, 2, figsize=(8, 10), gridspec_kw={"width_ratios": [3, 1]})
    fig.preview_ax = preview_ax
  else:
    fig = ax.figure
    preview_ax = fig._preview_ax

  display_board = game.board.copy()

  tetromino = game.active_tetromino.shape

  for r in range(tetromino.shape[0]):
    for c in range(tetromino.shape[1]):

      if tetromino[r, c] != 0:

        board_row = game.current_row + r
        board_col = game.current_col + c

        if 0 <= board_row < display_board.shape[0]:
          if 0 <= board_col < display_board.shape[1]:
            display_board[board_row, board_col] = tetromino[r, c]

  color_map = ListedColormap(TETROMINO_COLORS)

  ax.clear()

  ax.imshow(display_board, cmap=color_map, vmin=0, vmax=7)

  ax.set_xticks(np.arange(-0.5, 10, 1), minor = True)
  ax.set_yticks(np.arange(-0.5, 20, 1), minor = True)

  ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)

  ax.set_xticks([])
  ax.set_yticks([])

  if game.is_game_over:
    ax.set_title(f"GAME OVER\nScore: {game.score}", fontsize=18, color="red")
  else:
    ax.set_title(f"Score: {game.score} | Lines Cleared: {game.total_lines_cleared}", fontsize=14)

  ax.set_aspect("equal")

  fig.tight_layout()
  draw_next_tetromino(game, preview_ax)
  return fig, ax
