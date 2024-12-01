# utilities/screen_capture.py
import cv2
import numpy as np
import pyautogui
from mss import mss
import logging
import pygetwindow as gw

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_game_region(window_title):
    """
    Retrieves the screen region of the specified window title.
    """
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        return {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
    except Exception as e:
        logging.error(f"Error getting game window region for {window_title}: {e}")
        return None

def capture_screen(window_title=None):
    """
    Captures the entire screen or a specific window if a title is provided.
    """
    try:
        if window_title:
            region = get_game_region(window_title)
            if not region:
                raise ValueError(f"Window titled '{window_title}' not found.")
            with mss() as sct:
                screen = np.array(sct.grab(region))
                logging.info(f"Captured screen of {window_title}")
                return screen
        else:
            return np.array(pyautogui.screenshot())
    except Exception as e:
        logging.error(f"Error capturing screen: {e}")
        return None
