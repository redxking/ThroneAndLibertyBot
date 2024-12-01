# utilities/input_handler.py
import pyautogui
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def press_key(key):
    """
    Simulates a key press.
    """
    try:
        pyautogui.press(key)
        logging.info(f"Pressed key: {key}")
    except Exception as e:
        logging.error(f"Error pressing key {key}: {e}")
        raise

def hold_key(key, duration=1):
    """
    Simulates holding a key for a duration.
    """
    try:
        logging.info(f"Holding key: {key} for {duration}s")
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        logging.info(f"Released key: {key}")
    except Exception as e:
        logging.error(f"Error holding key {key}: {e}")
        raise

def perform_action(action, window_title=None):
    """
    Performs a specific action by simulating input.
    """
    actions = {
        "move_forward": lambda: hold_key("w", duration=1),
        "move_backward": lambda: hold_key("s", duration=1),
        "move_left": lambda: hold_key("a", duration=1),
        "move_right": lambda: hold_key("d", duration=1),
        "jump": lambda: press_key("space"),
        "attack": lambda: press_key("e"),
        "find_target": lambda: press_key("tab"),
        "use_skill_1": lambda: press_key("1"),
        "use_skill_2": lambda: press_key("2"),
        "use_skill_3": lambda: press_key("3"),
        "use_skill_4": lambda: press_key("4"),
        "rotate_left": lambda: hold_key("left", duration=0.5),
        "rotate_slow_right": lambda: hold_key("right", duration=0.5),
    }

    try:
        if window_title:
            from utilities.focus_window import ensure_game_window_focused
            focused = ensure_game_window_focused(window_title)
            if not focused:
                logging.error(f"Failed to focus on window: {window_title}")
                return

        if action in actions:
            logging.info(f"Performing action: {action}")
            actions[action]()
        else:
            logging.error(f"Unknown action: {action}")
            raise ValueError(f"Unknown action: {action}")
    except Exception as e:
        logging.error(f"Error performing action {action}: {e}")
        raise
