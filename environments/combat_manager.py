import time
import logging

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
        logging.info("Target acquired.")

    def calculate_combat_reward(self, current_health):
        """
        Calculates the combat reward based on target health changes.
        """
        combat_reward = 0
        kill_reward = 0

        if self.previous_target_health is not None:
            health_difference = self.previous_target_health - current_health

            if current_health == 0.0:
                self.target_killed = True
                time_to_kill = time.time() - self.target_acquired_time
                kill_reward = max(50 - time_to_kill * 2, 10)
                logging.info(f"Target killed in {time_to_kill:.2f} seconds. Kill Reward: {kill_reward}")
            elif health_difference > 0:
                combat_reward = health_difference * 20
                logging.debug(f"Damage dealt: {health_difference}. Combat Reward: {combat_reward}")
            elif current_health > 0 and not self.target_killed:
                combat_reward = -10
                logging.debug("Prolonged engagement without kill. Combat Penalty: -10")

        self.previous_target_health = current_health
        return combat_reward, kill_reward

    def missed_target_penalty(self):
        """
        Apply a penalty if a target is ignored or passed without killing.
        """
        if not self.target_killed and self.target_acquired_time is not None:
            logging.info("Missed target penalty applied.")
            return -20
        return 0
