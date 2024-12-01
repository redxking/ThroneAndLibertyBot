import cv2
import numpy as np
import logging


class HUDManager:
    def __init__(self, hud_regions=None):
        if hud_regions is None:
            # Set default hud_regions if necessary
            self.hud_regions = {
                "player_hud": {"start": (28, 60), "width": 309, "height": 116},
                "target_hud": {"start": (339, 59), "width": 232, "height": 119},
            }
        else:
            self.hud_regions = hud_regions
        # Define specific health bar locations within the HUDs
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

    def process_target_hud(self, screen):
        """
        Process the target's HUD to extract health data.
        """
        target_hud = self.extract_hud(screen, self.hud_regions["target_hud"])
        if target_hud is None:
            return {"health": 0.0}

        health_bar_region = self.health_bar_regions["target_health"]
        health_bar = self.extract_hud(target_hud, health_bar_region)

        return {"health": self.process_health_bar(health_bar)}
