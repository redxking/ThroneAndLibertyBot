# test_env_initialization.py

import logging
from environments.throne_env import ThroneAndLibertyEnv


def main():
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("test_env.log"),
            logging.StreamHandler()
        ]
    )

    try:
        # Instantiate the environment with the required parameters
        env = ThroneAndLibertyEnv(window_title="TL 1.281.22.935", resized_size=(160, 90))
        logging.info("Environment initialized successfully.")

        # Reset the environment and get the initial observation
        initial_state, info = env.reset()
        logging.info(f"Initial Observation: {initial_state}")

        # Perform a single step with a dummy action
        dummy_action = env.action_space.sample()
        state, reward, terminated, truncated, info = env.step(dummy_action)
        logging.info(
            f"Step Output: State={state}, Reward={reward}, Terminated={terminated}, Truncated={truncated}, Info={info}")

    except Exception as e:
        logging.error(f"Error initializing environment: {e}")


if __name__ == "__main__":
    main()
