# agents/ppo_agent.py

import os
import logging
import numpy as np
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback, EvalCallback
from sb3_contrib import RecurrentPPO
from sb3_contrib.ppo_recurrent import CnnLstmPolicy  # Corrected import
from environments.throne_env import ThroneAndLibertyEnv  # Main environment

def create_wrapped_env(window_title="TL 1.281.22.935", n_envs=1, resized_size=(160, 90)):
    """
    Creates and wraps the ThroneAndLiberty environment consistently.

    Args:
        window_title (str): Title of the game window to capture.
        n_envs (int): Number of parallel environments.
        resized_size (tuple): Desired size for resized observations.

    Returns:
        VecTransposeImage: Wrapped vectorized environment.
    """
    env = make_vec_env(
        lambda: ThroneAndLibertyEnv(window_title=window_title, resized_size=resized_size),
        n_envs=n_envs
    )
    env = VecTransposeImage(env)
    return env

class TQDMCallback(BaseCallback):
    """
    Custom callback for monitoring training progress with a progress bar.
    """

    def __init__(self, total_timesteps, verbose=0):
        super().__init__(verbose)
        self.total_timesteps = total_timesteps
        self.progress_bar = None

    def _on_training_start(self):
        from tqdm import tqdm
        self.progress_bar = tqdm(total=self.total_timesteps, desc="Training Progress")
        logging.info("Training has started.")

    def _on_step(self):
        if self.progress_bar:
            self.progress_bar.update(1)
        return True

    def _on_training_end(self):
        if self.progress_bar:
            self.progress_bar.close()
        logging.info("Training has ended.")

def preprocess_observation(observation):
    """
    Preprocess observation by normalizing the image.

    Args:
        observation (np.ndarray): Raw observation image.

    Returns:
        np.ndarray: Normalized observation.
    """
    try:
        # Normalize the image to [0, 1]
        observation = observation.astype(np.float32) / 255.0
        return observation
    except Exception as e:
        logging.error(f"Error in preprocess_observation: {e}")
        return np.zeros((90, 160, 3), dtype=np.float32)  # Adjusted size to match resized_size

def load_model_if_exists(model_path, env):
    """
    Loads an existing model if available; otherwise, initializes a new one.

    Args:
        model_path (str): Path to the model file.
        env (VecTransposeImage): The environment to associate with the model.

    Returns:
        RecurrentPPO: Loaded or newly initialized model.
    """
    if os.path.exists(model_path + ".zip"):
        try:
            model = RecurrentPPO.load(model_path, env=env)
            logging.info(f"Loaded existing model from {model_path}")
            return model
        except Exception as e:
            logging.error(f"Error loading model from {model_path}: {e}")
            logging.info("Initializing a new Recurrent PPO model.")
    # Initialize a new Recurrent PPO model with a recurrent policy
    model = RecurrentPPO(
        CnnLstmPolicy,
        env,
        verbose=1,
        learning_rate=0.0003,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        tensorboard_log="./ppo_tensorboard/"  # Ensure this path is correct
    )
    logging.info("Initialized a new Recurrent PPO model.")
    return model

def train_ppo(total_timesteps=5000, model_path="data/models/ppo_throne_liberty"):
    """
    Trains the PPO agent.

    Args:
        total_timesteps (int): Number of timesteps to train.
        model_path (str): Path to save the trained model.

    Returns:
        RecurrentPPO: Trained model.
    """
    logging.info("Starting Training...")

    # Initialize the training environment
    logging.info("Initializing Training Environment...")
    env = create_wrapped_env()

    # Load or initialize model
    model = load_model_if_exists(model_path, env)

    # Initialize the evaluation environment with the same wrappers
    logging.info("Initializing Evaluation Environment...")
    eval_env = create_wrapped_env()

    # Define callbacks
    training_callback = TQDMCallback(total_timesteps)
    checkpoint_callback = CheckpointCallback(
        save_freq=1000,
        save_path=os.path.dirname(model_path),
        name_prefix="ppo_checkpoint"
    )
    eval_callback = EvalCallback(
        eval_env=eval_env,
        best_model_save_path=os.path.join(os.path.dirname(model_path), 'best_model'),
        log_path=os.path.join(os.path.dirname(model_path), 'logs'),
        eval_freq=5000,
        deterministic=True,
        render=False
    )
    callbacks = [training_callback, checkpoint_callback, eval_callback]

    try:
        logging.info(f"Training for {total_timesteps} timesteps...")
        print("Before model.learn()")  # Debug print
        model.learn(total_timesteps=total_timesteps, callback=callbacks)
        print("After model.learn()")  # Debug print
        logging.info("Training completed successfully.")
        model.save(model_path)
        logging.info(f"Model saved at {model_path}.zip")
    except Exception as e:
        logging.error(f"An error occurred during training: {e}")
        return model

    return model

def test_ppo(model_path, num_episodes=5):
    """
    Tests the trained PPO agent.

    Args:
        model_path (str): Path to the trained model.
        num_episodes (int): Number of episodes to test.

    Returns:
        None
    """
    logging.info("Starting Testing...")

    # Initialize the testing environment
    logging.info("Initializing Testing Environment...")
    test_env = create_wrapped_env()

    try:
        # Load the trained model
        model = RecurrentPPO.load(model_path, env=test_env)
        logging.info(f"Loaded model from {model_path}")
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return

    for episode in range(1, num_episodes + 1):
        state, info = test_env.reset()
        total_reward = 0
        terminated = False
        truncated = False
        step = 0
        hidden_states = None  # Initialize hidden states for RNN
        try:
            while not (terminated or truncated) and step < 1000:
                processed_state = preprocess_observation(state)
                # Expand dimensions to match the expected input shape (batch_size, height, width, channels)
                processed_state = np.expand_dims(processed_state, axis=0)
                action, hidden_states = model.predict(processed_state, state=hidden_states, deterministic=True)
                state, reward, terminated, truncated, info = test_env.step(action)
                total_reward += reward
                step += 1
            logging.info(f"Episode {episode} finished with total reward: {total_reward}")
        except Exception as e:
            logging.error(f"Error during testing: {e}")
            break

    logging.info("Testing Complete.")
