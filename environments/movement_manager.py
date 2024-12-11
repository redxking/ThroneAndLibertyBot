import numpy as np
import logging

class MovementManager:
    """
    Tracks and rewards meaningful player movement.
    """

    def __init__(self):
        self.position_history = []
        self.visited_positions = set()
        self.current_goal = None

    def reset(self):
        """
        Reset the movement manager's state for a new episode.
        """
        self.position_history = []
        self.visited_positions = set()
        self.current_goal = None

    def update_position(self, position):
        """
        Update the position history and track visited positions.
        Args:
            position (tuple): Current (x, y) position.
        """
        self.position_history.append(position)
        self.visited_positions.add(position)
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
            previous_position = self.position_history[-2]
            distance_moved = np.linalg.norm(np.array(previous_position) - np.array(last_position))
            if distance_moved > 15:
                logging.debug(f"Meaningful movement detected. Distance moved: {distance_moved}")
                return 10  # Reward for significant movement
            elif 5 < distance_moved <= 15:
                logging.debug(f"Moderate movement detected. Distance moved: {distance_moved}")
                return 5  # Smaller reward for moderate movement
            elif distance_moved < 2:
                logging.debug(f"Inefficient movement detected. Distance moved: {distance_moved}")
                return -20  # Penalize being stuck or moving inefficiently
        return 0

    def calculate_exploration_reward(self, state):
        """
        Encourage exploration by rewarding the agent for visiting new areas.
        Args:
            state (dict): Current state information.
        Returns:
            float: Exploration reward.
        """
        current_position = state.get("player_position", (0, 0))
        if current_position not in self.visited_positions:
            logging.debug(f"New area explored: {current_position}")
            self.visited_positions.add(current_position)
            return 15  # Reward for exploring a new area
        return 0

    def set_goal(self, goal_type, goal_position=None):
        """
        Set a movement goal.
        Args:
            goal_type (str): Type of movement goal ('explore', 'target', 'waypoint').
            goal_position (tuple): Position to move toward (x, y).
        """
        self.current_goal = {"type": goal_type, "position": goal_position}
        logging.info(f"Set movement goal: {self.current_goal}")

    def move_toward(self, current_position):
        """
        Generate movement action to approach the goal.
        Args:
            current_position (tuple): Current player position (x, y).
        Returns:
            str: Suggested movement action ('move_forward', 'rotate_left', etc.).
        """
        if not self.current_goal:
            return "explore"

        goal_position = self.current_goal["position"]
        if goal_position:
            vector_to_goal = np.array(goal_position) - np.array(current_position)
            distance = np.linalg.norm(vector_to_goal)

            if distance < 10:
                logging.info("Reached goal.")
                self.current_goal = None
                return "stop"

            angle_to_goal = np.arctan2(vector_to_goal[1], vector_to_goal[0])
            if -np.pi / 4 < angle_to_goal < np.pi / 4:
                return "move_forward"
            elif angle_to_goal > np.pi / 4:
                return "rotate_left"
            elif angle_to_goal < -np.pi / 4:
                return "rotate_right"
        return "move_forward"
