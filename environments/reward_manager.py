class RewardManager:
    def __init__(self, hud_manager, movement_manager, combat_manager):
        self.hud_manager = hud_manager
        self.movement_manager = movement_manager
        self.combat_manager = combat_manager

    def calculate_reward(self, state):
        total_reward = 0

        # Health-related rewards
        if "player_hud_data" in state:
            health = state["player_hud_data"].get("health", 0)
            if health >= 0.9:
                total_reward += 10  # High health is good
            elif health <= 0.4:
                total_reward -= 5  # Low health incurs minor penalty

        # Combat rewards
        if "target_hud_data" in state:
            current_health = state["target_hud_data"].get("health", 1.0)
            combat_reward = self.combat_manager.calculate_combat_reward(current_health)
            total_reward += combat_reward

        # Movement rewards via movement_manager
        if "message_hud_data" in state and state["message_hud_data"] == "Cannot move":
            total_reward -= 20  # Penalty for being unable to move
        else:
            movement_reward = self.movement_manager.calculate_movement_reward()
            total_reward += movement_reward

        # Penalty for missed targets
        missed_target_penalty = self.combat_manager.missed_target_penalty()
        total_reward += missed_target_penalty

        # Goal reached rewards
        if "info" in state and state["info"].get("goal_reached"):
            total_reward += 85

        return total_reward
