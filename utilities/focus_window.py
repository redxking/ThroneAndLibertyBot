# utilities/focus_window.py
import cv2
import numpy as np
from mss import mss
import pygetwindow as gw
import logging

logging.basicConfig(level=logging.INFO)


def focus_game_window(window_title="TL 1.261.22.810"):
    """
    Ensures the specified game window is focused and captures an adjusted screenshot
    for visual confirmation.

    Args:
        window_title (str): Title of the game window to focus.
    """
    try:
        # Retrieve the game window
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"Game window '{window_title}' not found.")
            return False

        game_window = windows[0]

        # Activate the game window if not already focused
        if not game_window.isActive:
            game_window.activate()
            logging.info(f"Focused game window: '{window_title}'")

        # Define capture region based on window geometry
        monitor = {
            "top": game_window.top + 36,  # Exclude the title bar (~36 pixels)
            "left": game_window.left,
            "width": game_window.width,
            "height": game_window.height - 36 + 25  # Include bottom (~25 pixels)
        }

        # Capture the game window
        with mss() as sct:
            screen = np.array(sct.grab(monitor))
            screen_bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)

            # Save and display the screenshot
            cv2.imwrite("game_window_adjusted.png", screen_bgr)
            logging.info("Saved adjusted game window screenshot as 'game_window_adjusted.png'.")
            cv2.imshow("Game Window (Adjusted)", screen_bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return True
    except Exception as e:
        logging.error(f"Error focusing and capturing game window '{window_title}': {e}")
        return False


def bring_window_to_front(window_title="TL 1.261.22.810"):
    """
    Bring the game window to the front if it's minimized.

    Args:
        window_title (str): The title of the game window to bring to the front.
    """
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"Game window '{window_title}' not found.")
            return False

        game_window = windows[0]
        if game_window.isMinimized:
            game_window.restore()
        game_window.activate()
        logging.info(f"Game window '{window_title}' is now active and brought to the front.")
        return True
    except Exception as e:
        logging.error(f"Error bringing game window to front: {e}")
        return False


def verify_window_focus(window_title="TL 1.261.22.810"):
    """
    Verify that the game window is focused and ready for input.

    Args:
        window_title (str): The title of the game window to verify focus on.
    """
    try:
        active_window = gw.getActiveWindow()
        if active_window and window_title in active_window.title:
            logging.info(f"Verified: Game window '{window_title}' is focused.")
            return True
        else:
            logging.warning(f"Game window '{window_title}' is not focused.")
            return False
    except Exception as e:
        logging.error(f"Error verifying window focus: {e}")
        return False


def ensure_game_window_focused(window_title="TL 1.261.22.810"):
    """
    Ensures the specified game window is focused and active.

    Args:
        window_title (str): Title of the game window to focus.
    """
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"Window titled '{window_title}' not found.")
            return False

        game_window = windows[0]
        if not game_window.isActive:
            game_window.activate()
            logging.info(f"Focused window: '{window_title}'")
        return True
    except Exception as e:
        logging.error(f"Error focusing window '{window_title}': {e}")
        return False


if __name__ == "__main__":
    # Test the functionality
    if focus_game_window():
        logging.info("Game window successfully focused and captured.")
    else:
        logging.error("Failed to focus game window.")
