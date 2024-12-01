import unittest
import numpy as np
from environments.movement_manager import MovementManager


class TestMovementManager(unittest.TestCase):
    def setUp(self):
        self.movement_manager = MovementManager()

    def test_update_position(self):
        # Test initial position update
        self.movement_manager.update_position((10, 20))
        self.assertEqual(self.movement_manager.position_history, [(10, 20)])

        # Test multiple updates to position
        for i in range(10):
            self.movement_manager.update_position((i, i))

        self.assertEqual(len(self.movement_manager.position_history), 10)
        self.assertEqual(self.movement_manager.position_history[0], (0, 0))  # Corrected expected value
        self.assertEqual(self.movement_manager.position_history[-1], (9, 9))  # Ensure the last value matches

    def test_calculate_movement_reward(self):
        # Test no movement
        self.movement_manager.update_position((0, 0))
        self.assertEqual(self.movement_manager.calculate_movement_reward(), 0)

        # Test small movement (penalty case)
        self.movement_manager.update_position((1, 1))
        self.assertEqual(self.movement_manager.calculate_movement_reward(), -5)

        # Test large movement (reward case)
        self.movement_manager.update_position((15, 15))
        self.assertEqual(self.movement_manager.calculate_movement_reward(), 2)


if __name__ == '__main__':
    unittest.main()
