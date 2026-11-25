import random
from game.board import (create_board, is_valid, place_tetromino, line_clear, ROWS, COLS)
from game.tetrominos import TETROMINOS, Tetromino

class TetrisGame:
  def __init__(self):
    #initialize game board
    self.board = create_board()

    #track current game state
    self.total_lines_cleared = 0
    self.score = 0
    self.level = 1
    self.drop_interval = 500
    self.is_game_over = False

    self.upcoming_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))
    
    #create the first tetromino
    self.spawn_tetromino()

  def spawn_tetromino(self):
    #randomly select from one of the seven
    self.active_tetromino = self.upcoming_tetromino

    self.upcoming_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))

    #position the tetromino top of board
    self.current_row = 0
    self.current_col = (COLS - self.active_tetromino.shape.shape[1]) // 2

    #check if new Tetromino can spawn
    if not is_valid(self.board, self.active_tetromino.shape, self.current_row, self.current_col):
      self.is_game_over = True


  def move_left(self):
    if is_valid(self.board, self.active_tetromino.shape, self.current_row, self.current_col - 1):
      self.current_col -= 1


  def move_right(self):
    if is_valid(self.board, self.active_tetromino.shape, self.current_row, self.current_col + 1):
      self.current_col += 1


  def move_down(self):
    if is_valid(self.board, self.active_tetromino.shape, self.current_row + 1, self.current_col):
      self.current_row += 1
    else:
      self.lock_tetromino()


  def rotate_clockwise(self):
    original_shape = self.active_tetromino.shape.copy()
    self.active_tetromino.rotate_clockwise()

    if not is_valid(self.board, self.active_tetromino.shape, self.current_row, self.current_col):
      self.active_tetromino.shape = original_shape


  def rotate_counterclockwise(self):
    original_shape = self.active_tetromino.shape.copy()
    self.active_tetromino.rotate_counterclockwise()

    if not is_valid(self.board, self.active_tetromino.shape, self.current_row, self.current_col):
      self.active_tetromino.shape = original_shape


  def lock_tetromino(self):
    place_tetromino(self.board, self.active_tetromino.shape, self.current_row, self.current_col)

    self.board, lines_cleared = line_clear(self.board)
    self.total_lines_cleared += lines_cleared
    self.update_score(lines_cleared)
    self.update_level()

    self.spawn_tetromino()


  def hard_drop(self):
    while is_valid(self.board, self.active_tetromino.shape, self.current_row + 1, self.current_col):
      self.current_row += 1
    self.lock_tetromino()


  def update_score(self, lines_cleared):
    if lines_cleared == 1:
      self.score += 100
    elif lines_cleared == 2:
      self.score += 300
    elif lines_cleared == 3:
      self.score += 500
    elif lines_cleared == 4:
      self.score += 800


  def update_level(self):
    new_level = (self.total_lines_cleared // 10) + 1

    if new_level > self.level:
      self.level = new_level

      self.drop_interval = max(500 - (self.level - 1) * 50, 100)
