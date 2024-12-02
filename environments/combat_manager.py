# environments/combat_manager.py
class CombatManager:
    """
    Manages combat-related calculations and rewards.
    """
    def __init__(self):
        self.previous_target_health = None

    def reset(self):
        """
        Reset the combat manager's state for a new episode.
        """
        self.previous_target_health = None

    def calculate_combat_reward(self, current_health):
        """
        Calculates the reward based on target health changes.

        Args:
            current_health (float): Current health of the target.

        Returns:
            float: Calculated combat reward.
        """
        reward = 0
        if self.previous_target_health is not None:
            health_difference = self.previous_target_health - current_health
            if 0.0 < current_health < 0.1:
                reward += 15  # Reward for severely weakening the target
            elif current_health == 0.0:
                reward += 25  # Reward for killing the target
            elif health_difference > 0:
                reward += 5 * health_difference  # Reward proportional to damage dealt
        self.previous_target_health = current_health
        return reward
