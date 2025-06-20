#!/usr/bin/env python3
"""
Example usage of the Macrocosmos Logger.

This example demonstrates how to use the Logger class to:
1. Initialize a logging run
2. Log data and metrics
3. Capture Python logging and stdout/stderr
4. Finish the run and cleanup
"""

import logging
import time
from macrocosmos import Logger
from macrocosmos.resources._client import BaseClient


def main():
    # Create a client
    client = BaseClient(
        api_key="your-api-key-here", app_name="logger-example"
    )  # Replace with your actual API key

    # Create logger instance
    mcl = Logger(client)

    try:
        # Initialize the logger
        run_id = mcl.init(
            project="example-project",
            entity="example-entity",
            tags=["example", "demo"],
            notes="This is an example run",
            config={"learning_rate": 0.001, "batch_size": 32},
            name="example-run",
            description="An example logging run",
        )

        print(f"Started logging run with ID: {run_id}")

        # Simulate some training
        for epoch in range(5):
            # Simulate training metrics
            loss = 1.0 / (epoch + 1)  # Decreasing loss
            accuracy = 0.8 + (epoch * 0.04)  # Increasing accuracy

            # Log the metrics
            mcl.log(
                {
                    "epoch": epoch,
                    "loss": loss,
                    "accuracy": accuracy,
                    "learning_rate": 0.001,
                },
                step=epoch,
            )

            # Log some additional info
            logging.info(f"Completed epoch {epoch}")
            logging.warning(f"Loss is {loss:.4f}")

            # Simulate some stdout output
            print(f"Epoch {epoch}: Loss={loss:.4f}, Accuracy={accuracy:.4f}")

            time.sleep(1)  # Simulate training time

        # Log final results
        mcl.log({"final_loss": 0.2, "final_accuracy": 0.95, "total_epochs": 5}, step=5)

        print("Training completed successfully!")

    except Exception as e:
        print(f"Error during logging: {e}")
        logging.error(f"An error occurred: {e}")

    finally:
        # Always finish the logger
        mcl.finish()
        print("Logger finished and cleaned up")


if __name__ == "__main__":
    main()
