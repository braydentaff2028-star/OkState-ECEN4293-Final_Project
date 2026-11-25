import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from types import SimpleNamespace
from game.main import handle_keypress, update_game, AI_STRATEGIES, AI_PLACEMENT_STRATEGUES
from game.game_engine import TetrisGame
from game.tetrominos import Tetromino

def test_left_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_col = 4

  fig, ax = plt.subplots()
  event = SimpleNamespace(key="left")

  handle_keypress(event, game, ax)
  assert game.current_col == 3
  plt.close(fig)


def test_right_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_col = 3

  fig, ax = plt.subplots()
  event = SimpleNamespace(key="right")

  handle_keypress(event, game, ax)
  assert game.current_col == 4
  plt.close(fig)


def test_down_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0

  fig, ax = plt.subplots()
  event = SimpleNamespace(key="down")

  handle_keypress(event, game, ax)
  assert game.current_row == 1
  plt.close(fig)


def test_x_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(3)

  original_shape = game.active_tetromino.shape

  fig, ax = plt.subplots()
  event = SimpleNamespace(key = "x")

  handle_keypress(event, game, ax)

  expected_shape = np.rot90(original_shape, k=-1)
  assert np.array_equal(game.active_tetromino.shape, expected_shape)
  plt.close(fig)


def test_z_key():
  game = TetrisGame()
  game.active_tetromino = Tetromino(3)

  original_shape = game.active_tetromino.shape

  fig, ax = plt.subplots()
  event = SimpleNamespace(key = "z")

  handle_keypress(event, game, ax)

  expected_shape = np.rot90(original_shape, k=1)
  assert np.array_equal(game.active_tetromino.shape, expected_shape)
  plt.close(fig)


def test_hard_drop():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0
  game.current_col = 3

  fig, ax = plt.subplots()
  event = SimpleNamespace(key=" ")




  handle_keypress(event, game, ax)
  assert np.all(game.board[19, 3:7] == 1)
  plt.close(fig)
  
def test_auto_fall():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0

  fig, ax = plt.subplots()

  update_game(game, ax)

  assert game.current_row == 1
  plt.close(fig)


def test_auto_fall_after_game_over():
  game = TetrisGame()
  game.active_tetromino = Tetromino(1)
  game.current_row = 0
  game.is_game_over = True

  fig, ax = plt.subplots()

  update_game(game, ax)

  assert game.current_row == 0
  plt.close(fig)


def test_update_game_updates_animation_interval():
    game = TetrisGame()
    game.drop_interval = 450

    fig, ax = plt.subplots()

    animation = SimpleNamespace(
        event_source=SimpleNamespace(interval=500)
    )

    update_game(game, ax, animation)

    assert animation.event_source.interval == 450

    plt.close(fig)



def test_automated_mode_ignores_keyboard_input():
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)
    game.current_col = 4

    fig, ax = plt.subplots()
    event = SimpleNamespace(key="left")

    handle_keypress(event, game, ax, mode="automated")

    assert game.current_col == 4

    plt.close(fig)


def test_automated_mode_calls_selected_strategy(monkeypatch):
    game = TetrisGame()
    game.active_tetromino = Tetromino(1)

    fig, ax = plt.subplots()

    strategy_called = []

    def fake_strategy(game):
        strategy_called.append(True)

        return {
            "rotation": game.active_tetromino.shape,
            "row": 1,
            "col": 0
        }

    monkeypatch.setitem(
        AI_PLACEMENT_STRATEGIES,
        "Minimize Holes",
        fake_strategy
    )

    update_game(
        game,
        ax,
        mode="automated",
        strategy="Minimize Holes"
    )

    assert strategy_called == [True]
    assert game.current_row == 1

    plt.close(fig)


def test_back_to_menu_button_appears_on_game_over():
    game = TetrisGame()
    game.is_game_over = True

    fig, ax = plt.subplots()

    visibility = []

    menu_button = SimpleNamespace(
        ax=SimpleNamespace(
            set_visible=lambda visible: visibility.append(visible)
        )
    )

    update_game(
        game,
        ax,
        menu_button=menu_button
    )

    assert visibility == [True]

    plt.close(fig)


def test_animation_stops_on_game_over():
    game = TetrisGame()
    game.is_game_over = True

    fig, ax = plt.subplots()

    animation_stopped = []

    animation = SimpleNamespace(
        event_source=SimpleNamespace(
            stop=lambda: animation_stopped.append(True)
        )
    )

    update_game(
        game,
        ax,
        animation=animation
    )

    assert animation_stopped == [True]

    plt.close(fig)
