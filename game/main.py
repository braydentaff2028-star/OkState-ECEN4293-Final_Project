#Main for Tetris Game
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
from game.GUI import draw_game
from game.automation import (play_random_move, play_hole_minimization_move, play_height_minimization_move, play_combined_move)
from matplotlib.animation import FuncAnimation
from game.game_engine import TetrisGame
from game.GUI import draw_game


AI_STRATEGIES = {
    "Random": play_random_move,
    "Minimize Holes": play_hole_minimization_move,
    "Minimize Height": play_height_minimization_move,
    "Combined Optimization": play_combined_move
}

def handle_keypress(event, game, ax, mode="human"):
  if mode == "automated":
    return
    
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


def update_game(game, ax, animation = None, mode="human", strategy="Random"):
  if game.is_game_over:
    return

  if mode == "automated":
    AI_STRATEGIES[strategy](game)
  else:
    game.move_down()
  draw_game(game, ax)
  ax.figure.canvas.draw_idle()

  if animation is not None:
        animation.event_source.interval = game.drop_interval


def launch_game(mode, strategy):
  game = TetrisGame()

  fig, ax = draw_game(game)

  fig.canvas.mpl_connect(
    "key_press_event",
    lambda event: handle_keypress(event, game, ax, mode)
  )

  animation = FuncAnimation(
    fig,
    lambda frame: update_game(
      game,
      ax,
      animation,
      mode,
      strategy
    ),
    interval=game.drop_interval
  )

  fig.animation = animation

  plt.show()


def main():
  def main():
  menu_fig = plt.figure(figsize=(8, 6))
  menu_fig.suptitle("TETRIS", fontsize=24, fontweight="bold")

  # Game mode selection
  mode_ax = menu_fig.add_axes([0.15, 0.45, 0.3, 0.3])
  mode_ax.set_title("GAME MODE")

  mode_buttons = RadioButtons(
    mode_ax,
    ("Human", "Automated")
  )

  # AI strategy selection
  strategy_ax = menu_fig.add_axes([0.55, 0.35, 0.4, 0.45])
  strategy_ax.set_title("AI STRATEGY")

  strategy_buttons = RadioButtons(
    strategy_ax,
    (
      "Random",
      "Minimize Holes",
      "Minimize Height",
      "Combined Optimization"
    )
  )

  # Start button
  button_ax = menu_fig.add_axes([0.35, 0.12, 0.3, 0.1])

  start_button = Button(
    button_ax,
    "START GAME"
  )

  def start_game(event):
    selected_mode = mode_buttons.value_selected
    selected_strategy = strategy_buttons.value_selected

    if selected_mode == "Human":
      mode = "human"
    else:
      mode = "automated"

    plt.close(menu_fig)

    launch_game(mode, selected_strategy)

  start_button.on_clicked(start_game)

  plt.show()


if __name__ == "__main__":
  main()
