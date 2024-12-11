# tests/test_environment.py
from environments.throne_env import ThroneAndLibertyEnv
import logging


def test_environment():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("env_test.log"),
            logging.StreamHandler()
        ]
    )

    env = ThroneAndLibertyEnv()
    obs, info = env.reset()
    logging.info("Environment reset successfully.")

    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    logging.info(f"Performed action: {action}, Reward: {reward}, Done: {done}")


if __name__ == "__main__":
    test_environment()
