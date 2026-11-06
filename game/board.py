import numpy as np

#Dim of board
ROWS = 20
COLS = 10

def create_board():
  #create empty Tetris Board
  board = np.zeros((ROWS, COLS), dtype = int)

  return board

def is_valid(board, tetromino, row, col):
  #Checks if a Tetromino can legally occupy a space
  tetromino_rows, tetromino_cols = tetromino.shape

  for r in range(tetromino_rows):
    for c in range(tetromino_cols):

      #Ignore empty cells
      if tetromino[r, c] == 0:
        continue

      #calc board position
      board_row = row + r
      board_col = col + c

    #check left and right edges
      if board_col < 0 or board_col >= COLS:
        return False
      
    #check bottom edge
      if board_row >= ROWS:
        return False

    #check for overlapping tetrominos
      if board_row >= 0:
        if board[board_row, board_col] != 0:
          return False

  return True

def place_tetromino(board, tetromino, row, col):
  #place tetromino in an assumed valid position

  tetromino_rows, tetromino_cols = tetromino.shape

  for r in range(tetromino_rows):
    for c in range(tetromino_cols):

      if tetromino[r, c] != 0:

        board_row = row + r
        board_col = col + c

        if board_row >= 0:
          board[board_row, board_col = tetromino[r, c]

  return board


def line_clear(board):
  #Removes lines that have been completed across
  #Returns updated board and lines cleared in placement

  incomplete_rows = []

  for row in board:
    if not np.all(row != 0):
      incomplete_rows.append(row)

  rows_cleared = ROWS - len(incomplete_rows)
  empty_rows = np.zeros((rows_cleared, COLS), dtype=int)

  if rows_cleared > 0:
    board = np.vstack((empty_rows, incomplete_rows))

  return board, rows_cleared
  


  
