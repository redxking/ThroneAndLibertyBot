# utilities/input_handler.py
import pyautogui
import time
import logging
import pygetwindow as gw
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

def perform_action(action_name, window_title="TL 1.281.22.935"):
    """
    Executes the specified action in the game window.

    Args:
        action_name (str): The action to perform.
        window_title (str): The title of the game window.
    """
    try:
        # Bring the game window to the foreground
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"No window found with title '{window_title}'.")
            return
        window = windows[0]
        if window.isMinimized:
            window.restore()
        window.activate()
        time.sleep(0.1)  # Allow some time for the window to activate

        # Define action mappings
        action_mappings = {
            "move_forward": 'w',
            "move_backward": 's',
            "move_left": 'a',
            "move_right": 'd',
            "jump": 'space',
            "camera_up": 'up',  # Move camera angle up
            "camera_down": 'down',  # Move camera angle down
            "camera_left": 'left',  # Move camera angle left
            "camera_right": 'right',  # Move camera angle right
            "attack": 'leftclick',  # Perform attack
            "use_skill_1": '1',  # Cast skill 1
            "use_skill_2": '2',  # Cast skill 2
            "use_skill_3": '3',  # Cast skill 3
            "use_skill_4": '4',  # Cast skill 4
            "find_target": 'tab',  # Tab to find a target
            "interact": 'f'  # Interact with objects
        }

        keys = action_mappings.get(action_name, None)
        if keys is None:
            logging.warning(f"Unknown action '{action_name}'.")
            return

        if isinstance(keys, list):
            for key in keys:
                if key == 'leftclick':
                    pyautogui.click(button='left')
                else:
                    pyautogui.keyDown(key)
            time.sleep(0.1)  # Duration to hold the keys
            for key in keys:
                if key != 'leftclick':
                    pyautogui.keyUp(key)
        else:
            if keys == 'leftclick':
                pyautogui.click(button='left')
            else:
                pyautogui.keyDown(keys)
                time.sleep(0.1)
                pyautogui.keyUp(keys)

    except Exception as e:
        logging.error(f"Error performing action '{action_name}': {e}")
