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


def update_game(game, ax, animation=None, mode="human", strategy="Random", menu_button=None):
  if game.is_game_over:
    if menu_button is not None:
        menu_button.ax.set_visible(True)

    if animation is not None:
        animation.event_source.stop()

    ax.figure.canvas.draw_idle()
    return

  if mode == "automated":
    AI_STRATEGIES[strategy](game)
  else:
    game.move_down()
  draw_game(game, ax)
  ax.figure.canvas.draw_idle()
    
  if game.is_game_over:
    if menu_button is not None:
        menu_button.ax.set_visible(True)

    if animation is not None:
        animation.event_source.stop()

    ax.figure.canvas.draw_idle()
    return

  if animation is not None:
        animation.event_source.interval = game.drop_interval


def launch_game(mode, strategy):
  game = TetrisGame()

  fig, ax = draw_game(game)
  menu_ax = fig.add_axes([0.35, 0.02, 0.3, 0.06])

  menu_button = Button(
    menu_ax,
    "BACK TO MENU"
  )

  menu_ax.set_visible(False)

  def back_to_menu(event):
    plt.close(fig)
    main()

  menu_button.on_clicked(back_to_menu)

  fig.menu_button = menu_button

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
      strategy,
      menu_button
    ),
    interval=game.drop_interval
  )

  fig.animation = animation

  plt.show()



def main():
    menu_fig = plt.figure(figsize=(8, 6))
    menu_fig.suptitle("TETRIS", fontsize=24, fontweight="bold")

    # Game mode selection
    mode_ax = menu_fig.add_axes([0.3, 0.4, 0.4, 0.3])
    mode_ax.set_title("SELECT GAME MODE")

    mode_buttons = RadioButtons(
        mode_ax,
        ("Human", "Automated")
    )

    # Continue button
    continue_ax = menu_fig.add_axes([0.35, 0.15, 0.3, 0.1])

    continue_button = Button(
        continue_ax,
        "CONTINUE"
    )

    def select_mode(event):
        selected_mode = mode_buttons.value_selected

        # Human mode starts immediately
        if selected_mode == "Human":
            plt.close(menu_fig)
            launch_game("human", "Random")
            return

        # Remove the first menu
        mode_ax.remove()
        continue_ax.remove()

        # Display AI strategy selection
        strategy_ax = menu_fig.add_axes([0.25, 0.3, 0.5, 0.5])
        strategy_ax.set_title("SELECT AI STRATEGY")

        strategy_buttons = RadioButtons(
            strategy_ax,
            (
                "Random",
                "Minimize Holes",
                "Minimize Height",
                "Combined Optimization"
            )
        )

        # Start game button
        start_ax = menu_fig.add_axes([0.35, 0.12, 0.3, 0.1])

        start_button = Button(
            start_ax,
            "START GAME"
        )

        def start_automated_game(start_event):
            selected_strategy = strategy_buttons.value_selected

            plt.close(menu_fig)

            launch_game("automated", selected_strategy)

        start_button.on_clicked(start_automated_game)

        # Keep widget references alive
        menu_fig.strategy_buttons = strategy_buttons
        menu_fig.start_button = start_button

        menu_fig.canvas.draw_idle()

    continue_button.on_clicked(select_mode)

    # Keep widget references alive
    menu_fig.mode_buttons = mode_buttons
    menu_fig.continue_button = continue_button

    plt.show()


if __name__ == "__main__":
  main()
