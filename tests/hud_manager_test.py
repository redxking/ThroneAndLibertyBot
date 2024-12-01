import unittest
import numpy as np
from unittest.mock import MagicMock
from environments.hud_manager import HUDManager


class TestHUDManager(unittest.TestCase):
    def setUp(self):
        self.hud_manager = HUDManager()
        self.mock_screen = np.ones((1080, 1920, 3), dtype=np.uint8) * 255  # White mock screen

        # Create mock player health bar
        self.mock_player_health_bar = np.zeros((18, 207), dtype=np.uint8)
        self.mock_player_health_bar[:, :103] = 255  # 50% filled

        # Create mock target health bar
        self.mock_target_health_bar = np.zeros((20, 161), dtype=np.uint8)
        self.mock_target_health_bar[:, :81] = 255  # 50% filled

    def test_process_health_bar(self):
        health = self.hud_manager.process_health_bar(self.mock_player_health_bar)
        self.assertAlmostEqual(health, 0.5, places=2)

        health = self.hud_manager.process_health_bar(self.mock_target_health_bar)
        self.assertAlmostEqual(health, 0.5, places=2)

    def test_process_player_hud(self):
        # Mock extract_hud to return the player health bar
        self.hud_manager.extract_hud = MagicMock(return_value=self.mock_player_health_bar)

        player_data = self.hud_manager.process_player_hud(self.mock_screen)
        self.assertAlmostEqual(player_data["health"], 0.5, places=2)

    def test_process_target_hud(self):
        # Mock extract_hud to return the target health bar
        self.hud_manager.extract_hud = MagicMock(return_value=self.mock_target_health_bar)

        target_data = self.hud_manager.process_target_hud(self.mock_screen)
        self.assertAlmostEqual(target_data["health"], 0.5, places=2)


if __name__ == "__main__":
    unittest.main()
