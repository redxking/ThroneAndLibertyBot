# File: combat_manager_test.py
import unittest
from environments.combat_manager import CombatManager


class TestCombatManager(unittest.TestCase):
    def setUp(self):
        self.combat_manager = CombatManager()

    def test_calculate_combat_reward_no_previous_health(self):
        reward = self.combat_manager.calculate_combat_reward(0.5)
        self.assertEqual(reward, 0.0, "Reward should be 0 when no previous health is recorded.")

    def test_calculate_combat_reward_severely_weaken_target(self):
        self.combat_manager.previous_target_health = 0.5
        reward = self.combat_manager.calculate_combat_reward(0.05)
        self.assertEqual(reward, 15.0, "Reward should be 15 for severely weakening the target.")

    def test_calculate_combat_reward_kill_target(self):
        self.combat_manager.previous_target_health = 0.5
        reward = self.combat_manager.calculate_combat_reward(0.0)
        self.assertEqual(reward, 25.0, "Reward should be 25 for killing the target.")

    def test_calculate_combat_reward_damage_dealt(self):
        self.combat_manager.previous_target_health = 0.5
        reward = self.combat_manager.calculate_combat_reward(0.4)
        expected_reward = 5 * (0.5 - 0.4)  # Proportional reward
        self.assertAlmostEqual(
            reward, expected_reward,
            msg=f"Reward should be {expected_reward} for dealing damage."
        )


if __name__ == '__main__':
    unittest.main()
