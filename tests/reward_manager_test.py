import unittest
from unittest.mock import Mock

from environments.reward_manager import RewardManager


class RewardManagerTest(unittest.TestCase):
    def setUp(self):
        self.hud_manager = Mock()
        self.movement_manager = Mock()
        self.combat_manager = Mock()
        # Set default return values to 0
        self.movement_manager.calculate_movement_reward.return_value = 0
        self.combat_manager.calculate_combat_reward.return_value = 0
        self.reward_manager = RewardManager(self.hud_manager, self.movement_manager, self.combat_manager)

    def test_calculate_reward_health_penalty(self):
        state = {"player_hud_data": {"health": 0.4}}
        # movement reward is 0, combat reward is 0
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), -1.0, places=2)

    def test_calculate_reward_health_bonus(self):
        state = {"player_hud_data": {"health": 0.9}}
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), 10.0, places=2)

    def test_calculate_reward_combat_reward(self):
        self.combat_manager.calculate_combat_reward.return_value = 60
        state = {"target_hud_data": {"health": 0.3}}
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), 60.0, places=2)

    def test_calculate_reward_movement_reward(self):
        self.movement_manager.calculate_movement_reward.return_value = 10
        state = {"player_hud_data": {"health": 0.5}}  # Set health to avoid health bonus
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), 10.0, places=2)

    def test_calculate_reward_stuck_penalty(self):
        state = {"message_hud_data": "Cannot move"}
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), -20.0, places=2)

    def test_calculate_reward_goal_reward(self):
        state = {"info": {"goal_reached": True}}
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), 85.0, places=2)

    def test_calculate_reward_combined_rewards(self):
        self.combat_manager.calculate_combat_reward.return_value = 60
        self.movement_manager.calculate_movement_reward.return_value = 10
        state = {
            "player_hud_data": {"health": 0.6},
            "target_hud_data": {"health": 0.2},
            "message_hud_data": "Cannot move",
            "info": {"goal_reached": True},
        }
        expected_reward = 85 + 60 - 20  # Movement reward not added when stuck
        self.assertAlmostEqual(self.reward_manager.calculate_reward(state), expected_reward, places=2)


if __name__ == '__main__':
    unittest.main()
