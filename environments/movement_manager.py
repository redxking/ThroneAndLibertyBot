import numpy as np


class MovementManager:
    """
    Tracks and rewards meaningful player movement.
    """
    def __init__(self):
        self.position_history = []

    def update_position(self, position):
        """
        Update the position history with the current position.

        Args:
            position (tuple): Current (x, y) position.
        """
        self.position_history.append(position)
        if len(self.position_history) > 10:
            self.position_history.pop(0)  # Limit the history length

    def calculate_movement_reward(self):
        """
        Calculate movement reward based on position changes.

        Returns:
            float: Calculated movement reward.
        """
        if len(self.position_history) > 1:
            last_position = self.position_history[-1]
            current_position = self.position_history[-2]
            distance_moved = np.linalg.norm(np.array(current_position) - np.array(last_position))
            if distance_moved > 10:
                return 2  # Reward for meaningful movement
            elif distance_moved < 2:
                return -5  # Penalty for being idle or stuck
        return 0
