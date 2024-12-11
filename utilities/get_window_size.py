# utilities/get_window_size.py
import pygetwindow as gw
import logging

def get_game_window_size(window_title="TL 1.281.22.935"):
    """
    Retrieves the size of the specified game window.

    Args:
        window_title (str): The title of the game window.

    Returns:
        tuple: (width, height) of the window or None if not found.
    """
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"No window found with title: {window_title}")
            return None
        game_window = windows[0]
        width, height = game_window.width, game_window.height
        logging.info(f"Game window size: {width}x{height}")
        return (width, height)
    except Exception as e:
        logging.error(f"Error retrieving window size: {e}")
        return None

if __name__ == "__main__":
    size = get_game_window_size()
    if size:
        print(f"Game window size: {size[0]}x{size[1]}")
