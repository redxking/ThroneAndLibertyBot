import os
import logging
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.callbacks import BaseCallback
from environments.throne_env import ThroneAndLibertyEnv  # Main environment


class TQDMCallback(BaseCallback):
    """
    Custom callback for monitoring training progress.
    """
    def __init__(self, total_timesteps):
        super().__init__()
        self.total_timesteps = total_timesteps
        self.progress_bar = None

    def _on_training_start(self):
        from tqdm import tqdm
        self.progress_bar = tqdm(total=self.total_timesteps, desc="Training Progress")

    def _on_step(self):
        self.progress_bar.update(1)
        return True

    def _on_training_end(self):
        self.progress_bar.close()


def preprocess_observation(observation):
    """
    Preprocess observation by normalizing the image.
    """
    try:
        # Normalize the image to [0, 1]
        observation = observation.astype(np.float32) / 255.0
        return observation
    except Exception as e:
        logging.error(f"Error in preprocess_observation: {e}")
        return np.zeros((90, 160, 1), dtype=np.float32)


def train_ppo(total_timesteps=5000, log_interval=10):
    """
    Train the PPO agent using the ThroneAndLibertyEnv.
    """
    logging.info("Starting Training...")

    # Initialize the custom environment
    logging.info("Initializing Training Environment...")
    env = make_vec_env(lambda: ThroneAndLibertyEnv(), n_envs=1)
    env = VecTransposeImage(env)

    # Initialize the PPO model
    logging.info("Initializing PPO Model...")
    model = PPO("CnnPolicy", env, verbose=1, learning_rate=0.0003)

    # Define training progress callback
    callback = TQDMCallback(total_timesteps)

    model_path = "data/models/ppo_throne_liberty"
    try:
        # Train the model
        logging.info("Starting Training...")
        model.learn(total_timesteps=total_timesteps, callback=callback)
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model.save(model_path)
        logging.info(f"Training Complete. Model saved to {model_path}")
    except Exception as e:
        logging.error(f"Error during training: {e}")
        return

    # Test the model
    test_ppo(model_path)


def test_ppo(model_path):
    """
    Test the trained PPO agent.
    """
    logging.info("Starting Testing...")

    # Initialize the testing environment
    env = make_vec_env(lambda: ThroneAndLibertyEnv(), n_envs=1)
    env = VecTransposeImage(env)

    try:
        # Load the trained model
        model = PPO.load(model_path)
        logging.info(f"Loaded model from {model_path}")
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return

    obs = env.reset()
    total_reward = 0
    max_steps = 100

    try:
        for step in range(max_steps):
            obs = preprocess_observation(obs)
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
            total_reward += reward

            if terminated or truncated:
                logging.info(f"Episode finished with total reward: {total_reward}")
                obs = env.reset()
                total_reward = 0
    except Exception as e:
        logging.error(f"Error during testing: {e}")

    logging.info("Testing Complete.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    train_ppo(total_timesteps=5000)
