# environments/throne_env.py

import logging
import time

import gymnasium as gym
import numpy as np
import pyautogui
from gymnasium import spaces
from utilities.input_handler import perform_action
from environments.hud_manager import HUDManager
from environments.movement_manager import MovementManager
from environments.combat_manager import CombatManager
from environments.reward_manager import RewardManager

class ThroneAndLibertyEnv(gym.Env):
    """
    Custom Environment for the game Throne and Liberty.
    """

    metadata = {'render.modes': ['human']}

    def __init__(self, window_title="TL 1.281.22.935", resized_size=(160, 90)):
        """
        Initializes the ThroneAndLiberty Environment.

        Args:
            window_title (str): Title of the game window to capture.
            resized_size (tuple): Desired size for resized observations.
        """
        super().__init__()
        # Initialize managers with correct parameters
        self.hud_manager = HUDManager(
            hud_regions={
                "player_hud": {"start": (28, 60), "width": 309, "height": 116},
                "target_hud": {"start": (339, 59), "width": 232, "height": 119},
            },
            resized_size=resized_size,
            window_title=window_title
        )
        self.movement_manager = MovementManager()
        self.combat_manager = CombatManager()
        self.reward_manager = RewardManager(self.hud_manager, self.movement_manager, self.combat_manager)

        # Define observation and action spaces
        # Simplify to a single image observation to avoid nested spaces
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(resized_size[1], resized_size[0], 3),
            dtype=np.uint8
        )
        self.action_space = spaces.Discrete(16)

        # Initialize other necessary variables
        self.current_step = 0
        self.max_steps = 1000  # Example value, adjust as needed

    def reset(self, *, seed=None, options=None):
        """
        Resets the environment to an initial state and returns an initial observation.

        Returns:
            tuple: A tuple containing:
                - observation (np.ndarray): Initial screen observation.
                - info (dict): Additional info (empty in this case).
        """
        super().reset(seed=seed)
        # Reset managers
        self.movement_manager.reset()
        self.combat_manager.reset()
        # Clear any recurrent states if necessary
        state = self._get_state()
        return state["screen"], {}

    def step(self, action):
        """
        Executes one time step within the environment.

        Args:
            action (int): An action provided by the agent.

        Returns:
            tuple: A tuple containing:
                - observation (np.ndarray): Agent's observation of the current environment.
                - reward (float): Amount of reward returned after previous action.
                - terminated (bool): Whether the episode has ended.
                - truncated (bool): Whether the episode was truncated.
                - info (dict): Contains auxiliary diagnostic information.
        """
        try:
            # Map and execute the action
            if action is None:
                current_position = self._get_player_position()
                movement_action = self.movement_manager.move_toward(current_position)
                action = self._map_action_name_to_index(movement_action)
            action_name = self._map_action(action)
            logging.info(f"Performing action: {action_name}")
            perform_action(action_name, window_title=self.hud_manager.window_title)  # Use window_title from HUDManager

            # Get the current state
            state = self._get_state()

            # Check if a new target is acquired
            if state["target_hud_data"].get("health", 1.0) > 0 and not self.combat_manager.target_killed:
                self.combat_manager.target_acquired()

            # Calculate reward and check if the episode is done
            reward = self.reward_manager.calculate_reward(state)
            terminated = self._check_done(state)
            truncated = False  # You can set conditions for truncation if needed

            return state["screen"], reward, terminated, truncated, {}

        except Exception as e:
            logging.error(f"Error during step execution: {e}")
            # Return a random observation, negative reward, and end the episode
            return self.observation_space.sample(), -10, True, False, {}

    def _get_player_position(self):
        """
        Placeholder to retrieve the player's current position.
        Replace this with logic to detect the position from the HUD or other sources.

        Returns:
            tuple: (x, y) position of the player.
        """
        return (0, 0)  # Example position

    def _get_state(self):
        """
        Retrieve the current state by processing the HUD.

        Returns:
            dict: Current state containing screen observation and HUD data.
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
        action_mapping = {
            0: "move_forward",
            1: "move_backward",
            2: "move_left",
            3: "move_right",
            4: "jump",
            5: "camera_up",
            6: "camera_down",
            7: "attack",
            8: "use_skill_1",
            9: "use_skill_2",
            10: "use_skill_3",
            11: "use_skill_4",
            12: "find_target",
            13: "camera_left",
            14: "camera_right",
            15: "interact",
        }
        return action_mapping.get(action, "unknown_action")

    def _map_action_name_to_index(self, action_name):
        """
        Map a string action name to its corresponding index.

        Args:
            action_name (str): The action name.

        Returns:
            int: The corresponding action index.
        """
        action_mappings = {
            "move_forward": 'w',
            "move_backward": 's',
            "move_left": 'a',
            "move_right": 'd',
            "jump": 'space',
            "camera_up": 'up',  # Move camera angle up
            "camera_down": 'down',  # Move camera angle down
            "camera_left": 'left',  # Move camera angle left
            "camera_right": 'right',  # Move camera angle right
            "attack": 'leftclick',  # Perform attack
            "use_skill_1": '1',  # Cast skill 1
            "use_skill_2": '2',  # Cast skill 2
            "use_skill_3": '3',  # Cast skill 3
            "use_skill_4": '4',  # Cast skill 4
            "find_target": 'tab',  # Tab to find a target
            "interact": 'f'  # Interact with objects
        }
        return action_mappings.get(action_name, 0)  # Default to 0 if not found

    def _check_done(self, state):
        """
        Check if the episode is terminated.

        Args:
            state (dict): The current state.

        Returns:
            bool: True if the episode is terminated, False otherwise.
        """
        return state["player_hud_data"].get("health", 1.0) == 0.0

    def execute_action(self, action_name, gw=None):
        """
        Executes the specified action in the game window.

        Args:
            action_name (str): The action to perform.
        """
        try:
            # Bring the game window to the foreground
            windows = gw.getWindowsWithTitle(self.hud_manager.window_title)
            if not windows:
                logging.error(f"No window found with title '{self.hud_manager.window_title}'.")
                return
            window = windows[0]
            if window.isMinimized:
                window.restore()
            window.activate()
            time.sleep(0.1)  # Allow some time for the window to activate

            # Define action mappings
            action_mappings = {
                "move_forward": 'w',
                "move_backward": 's',
                "move_left": 'a',
                "move_right": 'd',
                "jump": 'space',
                "camera_up": 'up',  # Move camera angle up
                "camera_down": 'down',  # Move camera angle down
                "camera_left": 'left',  # Move camera angle left
                "camera_right": 'right',  # Move camera angle right
                "attack": 'leftclick',  # Perform attack
                "use_skill_1": '1',  # Cast skill 1
                "use_skill_2": '2',  # Cast skill 2
                "use_skill_3": '3',  # Cast skill 3
                "use_skill_4": '4',  # Cast skill 4
                "find_target": 'tab',  # Tab to find a target
                "interact": 'f'  # Interact with objects
            }

            keys = action_mappings.get(action_name, None)
            if keys is None:
                logging.warning(f"Unknown action '{action_name}'.")
                return

            if isinstance(keys, list):
                for key in keys:
                    if key == 'leftclick':
                        pyautogui.click(button='left')
                    else:
                        pyautogui.keyDown(key)
                time.sleep(0.1)  # Duration to hold the keys
                for key in keys:
                    if key != 'leftclick':
                        pyautogui.keyUp(key)
            else:
                if keys == 'leftclick':
                    pyautogui.click(button='left')
                else:
                    pyautogui.keyDown(keys)
                    time.sleep(0.1)
                    pyautogui.keyUp(keys)

        except Exception as e:
            logging.error(f"Error executing action '{action_name}': {e}")
