import time

class CombatManager:
    """
    Manages combat-related calculations and rewards.
    """
    def __init__(self):
        self.previous_target_health = None
        self.target_acquired_time = None
        self.target_killed = False

    def reset(self):
        """
        Reset the combat manager's state for a new episode.
        """
        self.previous_target_health = None
        self.target_acquired_time = None
        self.target_killed = False

    def target_acquired(self):
        """
        Mark the time a target was acquired.
        """
        self.target_acquired_time = time.time()
        self.target_killed = False

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
            if current_health == 0.0:
                # Target killed
                self.target_killed = True
                time_to_kill = time.time() - self.target_acquired_time
                reward += 50 - time_to_kill  # Reward for killing efficiently (less time = higher reward)
            elif health_difference > 0:
                reward += 10 * health_difference  # Reward proportional to damage dealt
            elif current_health > 0 and not self.target_killed:
                reward -= 10  # Penalty for not killing the target after engagement
        self.previous_target_health = current_health
        return reward

    def missed_target_penalty(self):
        """
        Apply a penalty if a target is ignored or passed without killing.
        """
        if not self.target_killed and self.target_acquired_time is not None:
            return -20  # Penalty for ignoring or failing to engage
        return 0
