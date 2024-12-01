import unittest
from unittest.mock import patch, Mock

import numpy as np
from environments.throne_env import ThroneAndLibertyEnv


class TestThroneAndLibertyEnv(unittest.TestCase):

    @patch('environments.throne_env.RewardManager')
    @patch('environments.throne_env.CombatManager')
    @patch('environments.throne_env.MovementManager')
    @patch('environments.throne_env.HUDManager')
    def test_init(self, MockHUDManager, MockMovementManager, MockCombatManager, MockRewardManager):
        env = ThroneAndLibertyEnv()
        self.assertIsNotNone(env.hud_manager)
        self.assertIsNotNone(env.movement_manager)
        self.assertIsNotNone(env.combat_manager)
        self.assertIsNotNone(env.reward_manager)
        self.assertIsNotNone(env.observation_space)
        self.assertIsNotNone(env.action_space)

    @patch('environments.throne_env.RewardManager')
    @patch('environments.throne_env.CombatManager')
    @patch('environments.throne_env.MovementManager')
    @patch('environments.throne_env.HUDManager')
    def test_reset(self, MockHUDManager, MockMovementManager, MockCombatManager, MockRewardManager):
        # Mock the reset methods
        MockMovementManager.return_value.reset.return_value = None
        MockCombatManager.return_value.reset.return_value = None
        # Mock get_screen_observation to return an np.ndarray
        MockHUDManager.return_value.get_screen_observation.return_value = np.zeros((90, 160, 1), dtype=np.uint8)

        env = ThroneAndLibertyEnv()
        initial_state, _ = env.reset()
        self.assertIsNotNone(initial_state)
        self.assertIsInstance(initial_state, np.ndarray)

    @patch('environments.throne_env.perform_action')
    @patch('environments.throne_env.RewardManager')
    @patch('environments.throne_env.CombatManager')
    @patch('environments.throne_env.MovementManager')
    @patch('environments.throne_env.HUDManager')
    def test_step(self, MockHUDManager, MockMovementManager, MockCombatManager, MockRewardManager, mock_perform_action):
        # Set up the mocks
        mock_perform_action.return_value = None
        MockRewardManager.return_value.calculate_reward.return_value = 0.0  # Set to float
        MockHUDManager.return_value.process_hud.return_value = {
            "player_hud": {"health": 1.0},
            "target_hud": {},
            "info": {}
        }
        MockHUDManager.return_value.get_screen_observation.return_value = np.zeros((90, 160, 1), dtype=np.uint8)

        env = ThroneAndLibertyEnv()
        observation, reward, terminated, _, _ = env.step(0)
        self.assertIsInstance(observation, np.ndarray)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(terminated, bool)

    @patch('environments.throne_env.RewardManager')
    @patch('environments.throne_env.CombatManager')
    @patch('environments.throne_env.MovementManager')
    @patch('environments.throne_env.HUDManager')
    def test_get_state(self, MockHUDManager, MockMovementManager, MockCombatManager, MockRewardManager):
        # Set up the mock
        MockHUDManager.return_value.process_hud.return_value = {
            "player_hud": {},
            "target_hud": {},
            "info": {}
        }
        MockHUDManager.return_value.get_screen_observation.return_value = np.zeros((90, 160, 1), dtype=np.uint8)

        env = ThroneAndLibertyEnv()
        state = env._get_state()
        self.assertIsInstance(state, dict)
        self.assertIn('screen', state)
        self.assertIn('player_hud_data', state)
        self.assertIn('target_hud_data', state)
        self.assertIn('info', state)

    @patch('environments.throne_env.RewardManager')
    @patch('environments.throne_env.CombatManager')
    @patch('environments.throne_env.MovementManager')
    @patch('environments.throne_env.HUDManager')
    def test_map_action(self, MockHUDManager, MockMovementManager, MockCombatManager, MockRewardManager):
        env = ThroneAndLibertyEnv()
        action_name = env._map_action(10)
        self.assertEqual(action_name, "use_skill_3")

    @patch('environments.throne_env.RewardManager')
    @patch('environments.throne_env.CombatManager')
    @patch('environments.throne_env.MovementManager')
    @patch('environments.throne_env.HUDManager')
    def test_check_done(self, MockHUDManager, MockMovementManager, MockCombatManager, MockRewardManager):
        env = ThroneAndLibertyEnv()
        done = env._check_done({"player_hud_data": {"health": 0.0}})
        self.assertTrue(done)


if __name__ == '__main__':
    unittest.main()
