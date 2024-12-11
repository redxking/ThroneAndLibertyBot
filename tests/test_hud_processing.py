# tests/test_hud_processing.py
from environments.hud_manager import HUDManager
import logging


def test_hud_processing():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to see detailed logs
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("hud_test.log"),
            logging.StreamHandler()
        ]
    )

    # Initialize HUDManager with correct window title
    hud_manager = HUDManager(
        hud_regions={
            "player_hud": {"start": (28, 60), "width": 309, "height": 116},
            "target_hud": {"start": (339, 59), "width": 232, "height": 119},
        },
        resized_size=(160, 90),
        window_title="TL 1.281.22.935"  # Replace with your actual window title
    )

    # Process HUD
    state = hud_manager.process_hud()
    print("Player Health:", state["player_hud"]["health"])
    print("Target Health:", state["target_hud"]["health"])


if __name__ == "__main__":
    test_hud_processing()
