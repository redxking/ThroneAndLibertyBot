# environments/reward_manager.py

import numpy as np
import logging

class RewardManager:
    def __init__(self, hud_manager, movement_manager, combat_manager):
        """
        Initializes the RewardManager with necessary components.

        Args:
            hud_manager (HUDManager): Instance managing HUD data extraction.
            movement_manager (MovementManager): Instance managing movement tracking and rewards.
            combat_manager (CombatManager): Instance managing combat-related rewards.
        """
        self.hud_manager = hud_manager
        self.movement_manager = movement_manager
        self.combat_manager = combat_manager

    def calculate_reward(self, state):
        """
        Calculates the total reward based on the current state.

        Args:
            state (dict): Current state information containing HUD data, spell usage, etc.

        Returns:
            float: Calculated and normalized reward.
        """
        total_reward = 0
        component_rewards = {}

        # 1. Survival Rewards
        if "player_hud_data" in state:
            health = state["player_hud_data"].get("health", 0)
            survival_reward = health * 10  # Encourage maintaining high health
            total_reward += survival_reward
            component_rewards["survival_reward"] = survival_reward

            if health <= 0.3 and health > 0:
                low_health_penalty = (0.3 - health) * 50  # Heavily penalize low health
                total_reward -= low_health_penalty
                component_rewards["low_health_penalty"] = -low_health_penalty
            elif health == 0:
                death_penalty = -500  # Massive penalty for death
                total_reward += death_penalty
                component_rewards["death_penalty"] = death_penalty

        # 2. Combat Efficiency Rewards
        if "target_hud_data" in state:
            current_health = state["target_hud_data"].get("health", 1.0)
            combat_reward, kill_reward = self.combat_manager.calculate_combat_reward(current_health)
            total_reward += combat_reward + kill_reward
            component_rewards["combat_reward"] = combat_reward
            component_rewards["kill_reward"] = kill_reward

        # 3. Movement Rewards
        if "message_hud_data" in state and state["message_hud_data"] == "Cannot move":
            movement_penalty = -100  # Heavily penalize inability to move
            total_reward += movement_penalty
            component_rewards["movement_penalty"] = movement_penalty
        else:
            movement_reward = self.movement_manager.calculate_movement_reward()
            total_reward += movement_reward
            component_rewards["movement_reward"] = movement_reward

        # 4. Spell Usage Rewards
        if "spell_usage_data" in state:
            spells_cast = state["spell_usage_data"].get("spells_cast", 0)
            effective_spells = state["spell_usage_data"].get("effective_spells", 0)
            wasted_spells = spells_cast - effective_spells

            effective_spells_reward = effective_spells * 15  # Reward for effective spells
            wasted_spells_penalty = wasted_spells * 5        # Penalize wasted spells

            total_reward += effective_spells_reward
            total_reward -= wasted_spells_penalty

            component_rewards["effective_spells_reward"] = effective_spells_reward
            component_rewards["wasted_spells_penalty"] = -wasted_spells_penalty

        # 5. Penalty for Missed Targets
        missed_target_penalty = self.combat_manager.missed_target_penalty()
        total_reward += missed_target_penalty  # Typically negative
        component_rewards["missed_target_penalty"] = missed_target_penalty

        # 6. Goal Achievement Rewards
        if "info" in state and state["info"].get("goal_reached"):
            goal_reward = 200  # Substantial reward for achieving goals
            total_reward += goal_reward
            component_rewards["goal_reward"] = goal_reward

        # 7. Encourage Exploration and Obstacle Navigation
        exploration_reward = self.movement_manager.calculate_exploration_reward(state)
        total_reward += exploration_reward
        component_rewards["exploration_reward"] = exploration_reward

        # 8. Time-based Rewards/Penalties
        if "info" in state and state["info"].get("episode_length"):
            episode_length = state["info"]["episode_length"]
            time_penalty = episode_length * 0.1  # Slight penalty for taking too long
            total_reward -= time_penalty
            component_rewards["time_penalty"] = -time_penalty

        # Normalize total_reward to prevent extreme values
        normalized_reward = np.clip(total_reward, -100, 200)  # Adjust bounds as needed
        component_rewards["normalized_reward"] = normalized_reward

        # Log all components for debugging
        logging.debug(f"Reward Components: {component_rewards}")
        return normalized_reward
