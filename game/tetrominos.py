import numpy as np

#seven different tetrominos
TETROMINOS = {
  
  #Hero
  1: np.array([
    [1, 1, 1, 1]
  ]),

  #Smashboy
  2: np.array([
    [2, 2],
    [2, 2]
  ]),
  
  #TeeWee
  3: np.array([
    [0, 3, 0],
    [3, 3, 3]
  ]),
  
  #Rhode Island Z
  4: np.array([
    [0, 4, 4],
    [4, 4, 0]
  ]),
  
  #Cleveland Z
  5: np.array([
    [5, 5, 0],
    [0, 5, 5]
  ]),
  
  #Orange Ricky
  6: np.array([
    [6, 0],
    [6, 0],
    [6, 0],
    [6, 6]
  ]),
  
  #Blue Rickey
  7: np.array([
    [0, 7],
    [0, 7],
    [0, 7],
    [7, 7]
  ])

class Tetromino:
  def __init__(self, tetromino_id):
    #create tetromino using its id
    self.tetromino_id = tetromino_id
    self.shape = TETROMINOS[tetromino_id].copy()

  def rotate_clockwise(self):
    #rotates tetromino 90 degrees clockwise
    self.shape = np.rot90(self.shape, k=-1)

  def rotate_counterclockwise(self):
    #rotates tetromino 90 degrees counterclockwise
    self.shape = np.rot90(self.shape, k=1)
