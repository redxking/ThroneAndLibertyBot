# environments/hud_manager.py

import cv2
import numpy as np
import logging
from utilities.screen_capture import capture_screen
from utilities.get_window_size import get_game_window_size

class HUDManager:
    def __init__(self, hud_regions=None, resized_size=(160, 90), window_title="TL 1.281.22.935"):
        """
        Initializes the HUDManager with specified regions and scaling factors.

        Args:
            hud_regions (dict, optional): Custom HUD regions. Defaults to None.
            resized_size (tuple, optional): Desired size for resized observations. Defaults to (160, 90).
            window_title (str, optional): Title of the game window to capture. Defaults to "TL 1.281.22.935".
        """
        if hud_regions is None:
            self.hud_regions = {
                "player_hud": {"start": (28, 60), "width": 309, "height": 116},
                "target_hud": {"start": (339, 59), "width": 232, "height": 119},
            }
        else:
            self.hud_regions = hud_regions

        # Define health bar regions relative to each HUD
        self.health_bar_regions = {
            "player_health": {"start": (109 - 28, 96 - 60), "width": 207, "height": 18},  # Relative to player_hud
            "target_health": {"start": (371 - 339, 92 - 59), "width": 161, "height": 20},  # Relative to target_hud
        }

        # Retrieve the original game window size
        original_size = get_game_window_size(window_title=window_title)
        if original_size is None:
            logging.error("Failed to retrieve game window size. Using default original_size=(1920, 1080).")
            original_size = (1920, 1080)  # Fallback to a default size

        self.original_size = original_size
        self.resized_size = resized_size
        self.window_title = window_title  # Store window_title for use in perform_action

        # Calculate scaling factors
        self.scale_x = self.resized_size[0] / self.original_size[0]
        self.scale_y = self.resized_size[1] / self.original_size[1]

        logging.info(f"Scaling factors - X: {self.scale_x:.4f}, Y: {self.scale_y:.4f}")

        # Scale HUD regions with minimum width and height of 1
        for hud in self.hud_regions.values():
            original_start = hud["start"]
            original_width = hud["width"]
            original_height = hud["height"]

            scaled_start = (
                int(original_start[0] * self.scale_x),
                int(original_start[1] * self.scale_y)
            )
            scaled_width = max(int(original_width * self.scale_x), 1)  # Ensure at least 1
            scaled_height = max(int(original_height * self.scale_y), 1)  # Ensure at least 1

            hud["start"] = scaled_start
            hud["width"] = scaled_width
            hud["height"] = scaled_height

            logging.debug(f"Scaled HUD Region: Start={scaled_start}, Width={scaled_width}, Height={scaled_height}")

        # Scale health bar regions relative to each HUD with minimum width and height of 1
        self.scaled_health_bar_regions = {}
        for key, region in self.health_bar_regions.items():
            scaled_start = (
                int(region["start"][0] * self.scale_x),
                int(region["start"][1] * self.scale_y)
            )
            scaled_width = max(int(region["width"] * self.scale_x), 1)  # Ensure at least 1
            scaled_height = max(int(region["height"] * self.scale_y), 1)  # Ensure at least 1

            self.scaled_health_bar_regions[key] = {
                "start": scaled_start,
                "width": scaled_width,
                "height": scaled_height
            }

            logging.debug(f"Scaled Health Bar Region for {key}: Start={scaled_start}, Width={scaled_width}, Height={scaled_height}")

    def extract_hud(self, screen, region):
        """
        Extracts the specified HUD region from the screen.

        Args:
            screen (np.ndarray): The captured screen image.
            region (dict): The region to extract with 'start', 'width', and 'height'.

        Returns:
            np.ndarray or None: Extracted HUD image or None if invalid.
        """
        start_x, start_y = region["start"]
        end_x = start_x + region["width"]
        end_y = start_y + region["height"]

        logging.debug(f"Extracting HUD: Start=({start_x}, {start_y}), End=({end_x}, {end_y})")
        logging.debug(f"Screen size: {screen.shape[1]}x{screen.shape[0]}")

        # Adjust end coordinates if they exceed screen boundaries
        end_x = min(end_x, screen.shape[1])
        end_y = min(end_y, screen.shape[0])

        if end_x <= start_x or end_y <= start_y:
            logging.warning("Invalid HUD region after adjustment.")
            return None

        return screen[start_y:end_y, start_x:end_x]

    def process_health_bar(self, bar_image):
        """
        Calculates the health percentage from the health bar image.

        Args:
            bar_image (np.ndarray or None): The extracted health bar image.

        Returns:
            float: Health percentage [0.0, 1.0].
        """
        if bar_image is None or bar_image.size == 0:
            logging.info("Health bar image not found. Setting health to 0.0")
            return 0.0

        # Convert to grayscale if needed
        if len(bar_image.shape) == 3:
            bar_image = cv2.cvtColor(bar_image, cv2.COLOR_BGR2GRAY)

        # Threshold to isolate the filled portion of the bar
        _, thresholded = cv2.threshold(bar_image, 128, 255, cv2.THRESH_BINARY)

        filled_pixels = np.sum(thresholded == 255)
        total_pixels = thresholded.size

        return filled_pixels / total_pixels if total_pixels > 0 else 0.0

    def process_player_hud(self, screen):
        """
        Processes the player's HUD to extract health data.

        Args:
            screen (np.ndarray): The captured screen image.

        Returns:
            dict: Player health data.
        """
        player_hud = self.extract_hud(screen, self.hud_regions["player_hud"])
        if player_hud is None:
            return {"health": 0.0}

        health_bar_region = self.scaled_health_bar_regions["player_health"]
        health_bar = self.extract_hud(player_hud, health_bar_region)

        health_percentage = self.process_health_bar(health_bar)
        logging.debug(f"Player Health: {health_percentage:.2f}")
        return {"health": health_percentage}

    def process_target_hud(self, screen):
        """
        Processes the target's HUD to extract health data.

        Args:
            screen (np.ndarray): The captured screen image.

        Returns:
            dict: Target health data.
        """
        target_hud = self.extract_hud(screen, self.hud_regions["target_hud"])
        if target_hud is None:
            return {"health": 0.0}

        health_bar_region = self.scaled_health_bar_regions["target_health"]
        health_bar = self.extract_hud(target_hud, health_bar_region)

        health_percentage = self.process_health_bar(health_bar)
        logging.debug(f"Target Health: {health_percentage:.2f}")
        return {"health": health_percentage}

    def process_hud(self):
        """
        Processes the HUD data for the player and the target.

        Returns:
            dict: Combined HUD data.
        """
        try:
            screen = self.get_screen_observation()

            # Extract and process player HUD
            player_hud_data = self.process_player_hud(screen)

            # Extract and process target HUD
            target_hud_data = self.process_target_hud(screen)

            return {
                "player_hud": player_hud_data,
                "target_hud": target_hud_data,
                "info": {},  # Add additional info if needed
            }
        except Exception as e:
            logging.error(f"Error processing HUD: {e}")
            return {"player_hud": {}, "target_hud": {}, "info": {}}

    def get_screen_observation(self):
        """
        Captures the game window screen and preprocesses it for observations.

        Returns:
            np.ndarray: Preprocessed screen observation.
        """
        try:
            screen = capture_screen(window_title=self.window_title)
            if screen is not None:
                # Convert the image to BGR and resize
                color_screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
                resized_screen = cv2.resize(color_screen, self.resized_size)
                observation = resized_screen  # Shape: (resized_height, resized_width, 3)
                logging.debug(f"Resized screen shape: {observation.shape}")
                return observation
            else:
                logging.error("Failed to capture screen.")
                return np.zeros((*self.resized_size, 3), dtype=np.uint8)
        except Exception as e:
            logging.error(f"Error capturing screen observation: {e}")
            return np.zeros((*self.resized_size, 3), dtype=np.uint8)
