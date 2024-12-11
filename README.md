# ThroneAndLibertyBot: README

## Overview

**ThroneAndLibertyBot** is an AI-driven bot designed to play the MMORPG *Throne and Liberty*. It leverages machine learning, reinforcement learning (RL), and computer vision to navigate the game world, interact with in-game objects, and complete tasks autonomously. The bot uses the Proximal Policy Optimization (PPO) algorithm for learning optimal strategies and performs real-time actions in response to game states.

---

## Goals

- Automate gameplay, including navigation, combat, and task completion.
- Learn from game states and improve performance using reinforcement learning.
- Mimic human-like behaviors and decisions.
- Handle scenarios like getting stuck or dying and resuming tasks intelligently.

---

## **My Status**
Dec 11 2024: To continue with the reinforcement learning approach, I delved into some reading and discovered that I can set up multiple channels for the bot to learn about various aspects of its environment. Here’s a list of tasks I need to prioritize to start:

1. Target Identification: (Can we teach the bot to identify targets on the screen using the Tab key, similar to how humans do?)
2. Terrain Types: (Identify and distinguish between different types of terrain, such as water, grass, sand, and rock.)
3. Correctly Monitor Player and Target Health: (Develop a system to monitor the health of both players and targets accurately.)
4. Blocking Animation: (Identify and execute blocking animations, including how to detect them and use the skill effectively.)
5. Navigation: (Teach the bot to recognize and navigate through each section of the map. Ensure it understands how to move around different areas.)
6. Questing and Contracts: (Develop the ability for the bot to identify and interact with different types of injectives present in the game.)

The ultimate goal is to achieve this using reinforcement learning. While YOLO might be a more suitable approach initially, we aim to build this system to the point where it functions like a human, comprehending all aspects of the game without resorting to hacking the memory or any other unauthorized methods of injection.

---
## Directory Structure
Here’s an explanation of the bot’s directory structure and its components:

### **Main Files**
1. **`main.py`**: The entry point of the bot. Handles training and testing of the PPO agent. It initializes the environment and starts the reinforcement learning process using the `ppo_agent.py` module.

---

### **Environment**
2. **`throne_env.py`**: Defines the custom OpenAI Gym environment for *Throne and Liberty*. 
    - Manages HUD processing, action execution, and reward calculation.
    - Maps discrete actions (e.g., movement, combat) to corresponding in-game actions.
    - Tracks game state and terminates episodes when necessary.

---

### **Reinforcement Learning**
3. **`ppo_agent.py`**:
    - Implements the PPO algorithm using Stable-Baselines3.
    - Defines training and testing routines for the bot.
    - Uses callbacks to track training progress.

---

### **Utilities**
4. **`focus_window.py`**:
    - Ensures the game window is active and captures screenshots for debugging.
    - Functions include bringing the game to the foreground and verifying focus.

5. **`input_handler.py`**:
    - Simulates in-game actions using `pyautogui`.
    - Supports actions like movement, combat, and skill usage.

6. **`screen_capture.py`**:
    - Captures screenshots of the game screen or specific regions.
    - Helps extract observations for HUD analysis and model input.

---

### **Managers**
7. **`hud_manager.py`**:
    - Processes the game’s HUD (Heads-Up Display) to extract data like player health, target health, and other visual elements.
    - Calculates health percentages using image processing techniques.

8. **`movement_manager.py`**:
    - Tracks player movement and ensures meaningful progress.
    - Provides rewards for significant movement and penalizes idle states.

9. **`navigation_manager.py`**:
    - Handles pathfinding and navigation.
    - Includes logic to resolve "stuck" scenarios.

10. **`reward_manager.py`**:
    - Calculates rewards for actions based on combat, movement, and task completion.
    - Penalizes undesirable states, such as low health or inability to move.

11. **`combat_manager.py`**:
    - Handles combat logic and calculates rewards based on target health changes.
    - Rewards significant damage, kills, and weakening the target.

---

## How It Works

1. **Environment Initialization**:
   - The bot initializes the *Throne and Liberty* game environment (`ThroneAndLibertyEnv`) with observation and action spaces.

2. **Observation**:
   - Screenshots are captured in real-time, and the HUD is analyzed to extract game state information (e.g., health, target status).

3. **Action**:
   - Actions (e.g., movement, combat) are executed based on the PPO policy learned during training.

4. **Reward Calculation**:
   - Rewards are computed based on in-game progress, combat success, and movement effectiveness.

5. **Training**:
   - The PPO agent learns from interactions with the game, optimizing its policy for future decisions.

6. **Testing**:
   - The trained model is tested to evaluate performance and refine strategies.

---

## Getting Started

1. **Dependencies**:
   - Install required libraries using `pip install -r requirements.txt`.

2. **Run Training**:
   - Execute `main.py` to start training the bot.

3. **Run Testing**:
   - Use the `test_ppo` function in `main.py` to test the trained model.

4. **Debugging**:
   - Logs and screenshots are generated for analysis and debugging.

---

## Key Features

- **Dynamic HUD Processing**: Extracts vital in-game data using computer vision.
- **Reinforcement Learning**: Learns optimal gameplay strategies using PPO.
- **Modular Design**: Separate components for movement, combat, rewards, and navigation.
- **Error Handling**: Resilient to unexpected scenarios like being stuck or dying.
