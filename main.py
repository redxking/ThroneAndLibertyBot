# main.py
from agents.ppo_agent import train_ppo, test_ppo
import time
import logging

if __name__ == "__main__":
    # Configure logging to include timestamp and module details for debugging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    start_time = time.time()

    try:
        logging.info("Starting Training Process...")
        train_ppo(total_timesteps=5000)  # Specify total timesteps if needed
        logging.info("Training Process Complete. Proceeding to Testing Phase...")
        test_ppo(model_path="data/models/ppo_throne_liberty")  # Pass model path explicitly
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
    finally:
        elapsed_time = time.time() - start_time
        logging.info(f"All Processes Complete. Total Elapsed Time: {elapsed_time / 60:.2f} minutes.")
