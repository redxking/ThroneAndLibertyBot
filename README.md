Here’s a corrected version of the README.md with a properly formatted directory structure and a note about the game window title:

# Throne and Liberty Bot

This project is a reinforcement learning-based bot designed to play the game *Throne and Liberty*. The bot leverages object detection, screen captures, and interaction automation to navigate and interact with the game environment.

---

## Directory Structure

ThroneAndLibertyBot/
│
├── agents/
│   ├── ppo_agent.py          # PPO reinforcement learning agent
│   ├── dqn_agent.py          # DQN reinforcement learning agent
│
├── environments/
│   ├── throne_env.py         # Custom gym environment for the game
│
├── utilities/
│   ├── focus_window.py       # Ensures the game window is active
│   ├── input_handler.py      # Sends key and mouse inputs to the game
│   ├── screen_capture.py     # Captures screenshots of the game window
│   ├── health_bar_test.py    # Tests and validates the health bar coordinates
│
├── main.py                   # Main entry point for training the bot
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── game_window.png           # Example screenshot of the game window

---

## Setup Instructions

### 1. Prerequisites

- Install Python (version 3.8 or above recommended).
- Install the required dependencies using pip:

```bash
pip install -r requirements.txt

2. Setting Up the Game Environment

	•	Ensure the game Throne and Liberty is running in windowed mode.
	•	The game window title must match the current game version. For example:

TL 1.261.22.810

Update the focus_window.py script if the game window title changes in future versions.

3. Configuring Health Bar Coordinates

Before running the bot, validate the health bar coordinates to ensure accurate detection of the player and enemy health bars:

python utilities/health_bar_test.py

	•	Adjust the coordinates in throne_env.py if the detection is incorrect.

4. Running the Bot

To start training the bot using the PPO algorithm, run:

python main.py

File Descriptions

1. agents/ppo_agent.py

	•	Purpose: Implements the Proximal Policy Optimization (PPO) algorithm for training the bot.
	•	Key Functions:
	•	train_ppo(): Sets up the PPO model and starts the training process.
	•	Wraps the custom gym environment ThroneAndLibertyEnv.
	•	Uses a TQDM progress bar for real-time updates during training.
	•	Saves the trained model to the data/models directory.

2. agents/dqn_agent.py

	•	Purpose: Implements the Deep Q-Learning (DQN) algorithm for training the bot as an alternative to PPO.
	•	Key Functions:
	•	train_dqn(): Configures and trains the bot using the DQN algorithm.

3. environments/throne_env.py

	•	Purpose: Defines the custom OpenAI Gym/Gymnasium environment for Throne and Liberty.
	•	Key Components:
	•	__init__: Initializes the observation space (grayscale screen captures) and action space (discrete actions like movement, attacks).
	•	_get_state: Captures and processes the game screen into the observation space.
	•	_calculate_reward: Defines the reward system based on:
	•	Enemy health reduction (positive reward).
	•	Player health loss (penalty).
	•	Survival and death conditions.
	•	_is_stuck: Checks if the bot is stuck based on repeated positions.
	•	reset: Resets the environment at the start of each episode.
	•	step: Executes an action, calculates rewards, and checks for termination.

4. utilities/focus_window.py

	•	Purpose: Ensures the Throne and Liberty game window is active and focused.
	•	Key Function:
	•	focus_game_window(window_title): Finds and activates the game window using pygetwindow.

5. utilities/input_handler.py

	•	Purpose: Sends inputs to the game to simulate bot actions.
	•	Key Functions:
	•	perform_action(action, window_title): Maps an action to a corresponding key or mouse event and sends it to the game window.

6. utilities/screen_capture.py

	•	Purpose: Captures the game screen for processing and observation.
	•	Key Function:
	•	capture_game_window(): Captures the game window and resizes the image to match the observation space.

7. utilities/health_bar_test.py

	•	Purpose: Validates the detection of player and enemy health bars.
	•	Key Components:
	•	Extracts and saves regions of interest (ROIs) for health bars.
	•	Displays the captured health bars for visual confirmation.

8. main.py

	•	Purpose: Entry point for the bot’s training process.
	•	Key Components:
	•	Imports train_ppo() from ppo_agent.py to start training.
	•	Prints training progress and completion messages.

9. requirements.txt

	•	Purpose: Lists the Python dependencies required for the bot.
	•	Dependencies:
	•	stable-baselines3: Reinforcement learning algorithms.
	•	opencv-python: Image processing.
	•	numpy: Numerical computations.
	•	mss: Screen capture.
	•	pygetwindow: Window focus and activation.

10. game_window.png

	•	Purpose: Example screenshot of the game window to help validate screen captures and coordinate detection.

Usage Notes

	1.	Health Bar Validation:
	•	Ensure the health bar coordinates in throne_env.py are correct for your screen resolution by running health_bar_test.py.
	2.	Debugging Navigation:
	•	If the bot frequently gets stuck, check _calculate_reward and _is_stuck in throne_env.py for logic issues.
	3.	Action Mapping:
	•	Update input_handler.py if new actions are added to the bot’s capabilities.
	4.	Training Output:
	•	The trained model is saved in data/models. Use it to evaluate or test the bot’s performance in the game.

Future Enhancements

	1.	Obstacle Avoidance:
	•	Implement logic to detect and navigate around obstacles in the environment.
	2.	Camera Angle Normalization:
	•	Ensure the bot maintains a consistent camera angle for better navigation.
	3.	Expanded Goals:
	•	Add objectives like quest completion or resource collection.

This format renders the directory structure correctly and includes the required note about ensuring the game window title matches the current game version. Let me know if you'd like additional edits!