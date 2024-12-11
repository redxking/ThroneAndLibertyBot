# main.py

import logging
import sys


def main():
    # Configure logging at the very start
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("training.log"),  # Log to 'training.log' file
            logging.StreamHandler(sys.stdout)  # Also log to console
        ]
    )

    logging.info("Logging is configured successfully.")

    # Import training and testing functions
    from agents.ppo_agent import train_ppo, test_ppo

    model_path = "data/models/ppo_throne_liberty"
    total_timesteps_per_iteration = 5000  # Adjust as needed
    max_iterations = None  # Set to None for infinite training

    iteration = 0
    try:
        while True:
            iteration += 1
            logging.info(f"=== Training Iteration {iteration} ===")

            # Train the PPO agent
            model = train_ppo(
                total_timesteps=total_timesteps_per_iteration,
                model_path=model_path
            )

            # Optionally, perform testing every N iterations
            if iteration % 10 == 0:
                logging.info(f"=== Testing Iteration {iteration} ===")
                test_ppo(model_path=model_path)

            # Check if maximum iterations are reached
            if max_iterations and iteration >= max_iterations:
                logging.info("Reached maximum number of iterations. Exiting training loop.")
                break

    except KeyboardInterrupt:
        logging.info("Training interrupted by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        logging.info("Training process has ended.")


if __name__ == "__main__":
    main()
