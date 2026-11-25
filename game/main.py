#Main for Tetris Game
import matplotlib.pyplot as plt
from game.game_engine import TetrisGame
from game.GUI import draw_game

def handle_keypress(event, game, ax):
  if event.key == "left":
    game.move_left()
  elif event.key == "right":
    game.move_right()
  elif event.key == "down":
    game.move_down()
  elif event.key == "x":
    game.rotate_clockwise()
  elif event.key == "z":
    game.rotate_counterclockwise()
  elif event.key == " ":
    game.hard_drop()

  draw_game(game, ax)
  ax.figure.canvas.draw_idle()


def main():
  game = TetrisGame()
  fig, ax = draw_game(game)
  fig.canvas.mpl_connect("key_press_event", lambda event: handle_keypress(event, game, ax))
  plt.show()


if __name__ == "__main__":
  main()
