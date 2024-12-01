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
                total_reward += 10
            elif health <= 0.4:
                total_reward -= 1  # Adjusted from -10 to -1

        # Combat rewards via combat_manager
        if "target_hud_data" in state:
            combat_reward = self.combat_manager.calculate_combat_reward(state)
            total_reward += combat_reward

        # Movement rewards via movement_manager
        if "message_hud_data" in state and state["message_hud_data"] == "Cannot move":
            total_reward -= 20
            # Do not add movement reward when player cannot move
        else:
            movement_reward = self.movement_manager.calculate_movement_reward(state)
            total_reward += movement_reward

        # Goal reached rewards
        if "info" in state and state["info"].get("goal_reached"):
            total_reward += 85

        return total_reward
