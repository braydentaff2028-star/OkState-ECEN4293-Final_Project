#Main for Tetris Game
import matplotlib.pyplot as plt
from game.game_engine import TetrisGame
from game.GUI import draw_game

def main():
  game = TetrisGame()
  draw_game(game)
  plt.show()


if __name__ == "__main__":
  main()
