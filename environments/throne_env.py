import logging
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from utilities.input_handler import perform_action
from environments.hud_manager import HUDManager
from environments.movement_manager import MovementManager
from environments.combat_manager import CombatManager
from environments.reward_manager import RewardManager


class ThroneAndLibertyEnv(gym.Env):
    def __init__(self):
        super().__init__()
        # Initialize managers
        self.hud_manager = HUDManager(hud_regions={
            "player_hud": {"start": (28, 60), "width": 309, "height": 116},
            "target_hud": {"start": (339, 59), "width": 232, "height": 119},
        })
        self.movement_manager = MovementManager()
        self.combat_manager = CombatManager()
        self.reward_manager = RewardManager(self.hud_manager, self.movement_manager, self.combat_manager)

        # Define observation and action spaces
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(90, 160, 1), dtype=np.uint8
        )
        self.action_space = spaces.Discrete(15)

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        # Reset managers
        self.movement_manager.reset()
        self.combat_manager.reset()
        return self._get_state()["screen"], {}

    def step(self, action):
        try:
            # Map and execute the action
            action_name = self._map_action(action)
            logging.info(f"Performing action: {action_name}")
            perform_action(action_name, window_title="TL 1.261.22.810")

            # Get the current state
            state = self._get_state()

            # Check if a new target is acquired
            if state["target_hud_data"].get("health", 1.0) > 0 and not self.combat_manager.target_killed:
                self.combat_manager.target_acquired()

            # Calculate reward and check if the episode is done
            reward = self.reward_manager.calculate_reward(state)
            terminated = self._check_done(state)
            return state["screen"], reward, terminated, False, {}

        except Exception as e:
            logging.error(f"Error during step execution: {e}")
            return self.observation_space.sample(), -10, True, False, {}

    def _get_state(self):
        """
        Retrieve the current state by processing the HUD.
        """
        hud_data = self.hud_manager.process_hud()
        player_hud_data = hud_data.get("player_hud", {})
        target_hud_data = hud_data.get("target_hud", {})
        screen_observation = self.hud_manager.get_screen_observation()

        return {
            "screen": screen_observation,
            "player_hud_data": player_hud_data,
            "target_hud_data": target_hud_data,
            "info": hud_data.get("info", {})
        }

    def _map_action(self, action):
        """
        Map the discrete action index to a string action name.
        """
        action_mapping = {
            0: "move_forward",
            1: "move_backward",
            2: "move_left",
            3: "move_right",
            4: "jump",
            5: "rotate_left",
            6: "rotate_right",
            7: "attack",
            8: "use_skill_1",
            9: "use_skill_2",
            10: "use_skill_3",
            11: "use_skill_4",
            12: "find_target",
            13: "rotate_slow_left",
            14: "rotate_slow_right",
        }
        return action_mapping.get(action, "unknown_action")

    def _check_done(self, state):
        """
        Check if the episode is terminated.
        """
        return state["player_hud_data"].get("health", 1.0) == 0.0


if __name__ == "__main__":
    # Test environment initialization
    logging.basicConfig(level=logging.INFO)
    env = ThroneAndLibertyEnv()
    obs, _ = env.reset()
    logging.info(f"Environment initialized. Initial observation shape: {obs.shape}")
