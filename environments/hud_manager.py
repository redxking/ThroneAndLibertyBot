import cv2
import numpy as np
import logging
from utilities.screen_capture import capture_screen

class HUDManager:
    def __init__(self, hud_regions=None):
        if hud_regions is None:
            self.hud_regions = {
                "player_hud": {"start": (28, 60), "width": 309, "height": 116},
                "target_hud": {"start": (339, 59), "width": 232, "height": 119},
            }
        else:
            self.hud_regions = hud_regions

        self.health_bar_regions = {
            "player_health": {"start": (109, 96), "width": 207, "height": 18},
            "target_health": {"start": (371, 92), "width": 161, "height": 20},
        }

    def extract_hud(self, screen, region):
        """
        Extract the specified HUD region from the screen.
        """
        start_x, start_y = region["start"]
        end_x = start_x + region["width"]
        end_y = start_y + region["height"]

        if end_x > screen.shape[1] or end_y > screen.shape[0]:
            logging.warning("HUD region exceeds screen boundaries.")
            return None

        return screen[start_y:end_y, start_x:end_x]

    def process_health_bar(self, bar_image):
        """
        Calculate the health percentage from the health bar image.
        """
        if bar_image is None or bar_image.size == 0:
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
        Process the player's HUD to extract health data.
        """
        player_hud = self.extract_hud(screen, self.hud_regions["player_hud"])
        if player_hud is None:
            return {"health": 0.0}

        health_bar_region = self.health_bar_regions["player_health"]
        health_bar = self.extract_hud(player_hud, health_bar_region)

        return {"health": self.process_health_bar(health_bar)}

    def process_hud(self):
        """
        Process the HUD data for the player and the target.
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
        """
        try:
            # Replace 'TL 1.261.22.810' with your actual game window title
            screen = capture_screen(window_title="TL 1.261.22.810")
            if screen is not None:
                # Convert the image to grayscale and resize
                gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)
                resized_screen = cv2.resize(gray_screen, (160, 90))
                observation = resized_screen[:, :, np.newaxis]  # Add a channel dimension
                return observation
            else:
                logging.error("Failed to capture screen.")
                return np.zeros((90, 160, 1), dtype=np.uint8)
        except Exception as e:
            logging.error(f"Error capturing screen observation: {e}")
            return np.zeros((90, 160, 1), dtype=np.uint8)
