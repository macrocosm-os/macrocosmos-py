"""
Example demonstrating the Logger functionality with realistic usage patterns.
This example creates a run simulating actual application logging with predefined payload structures.
"""

import asyncio
import json
import random
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any

import macrocosmos as mc
from loguru import logger


# Run :
# MACROCOSMOS_BASE_URL=localhost:4000 MACROCOSMOS_CAPTURE_LOGS=true MACROCOSMOS_USE_HTTPS=false uv run examples/logger_example.py > tmp.log 2>&1
# pm2 start logger.config.js
def generate_training_metrics(epoch: int, total_epochs: int) -> Dict[str, Any]:
    """
    Generate realistic training metrics for a machine learning model.

    Args:
        epoch: Current epoch number
        total_epochs: Total number of epochs

    Returns:
        Dictionary with training metrics
    """
    # Simulate realistic training progress
    progress = epoch / total_epochs

    # Generate realistic loss curves (decreasing with some noise)
    base_loss = 2.0 * (1 - progress) + 0.1
    noise = random.uniform(-0.05, 0.05)
    loss = max(0.01, base_loss + noise)

    # Generate accuracy (increasing with some noise)
    base_accuracy = 0.3 + 0.6 * progress
    noise = random.uniform(-0.02, 0.02)
    accuracy = min(0.99, max(0.01, base_accuracy + noise))

    # Generate learning rate (typically decreases over time)
    lr = 0.001 * (1 - 0.8 * progress)

    return {
        "epoch": epoch,
        "total_epochs": total_epochs,
        "progress": progress,
        "loss": round(loss, 4),
        "accuracy": round(accuracy, 4),
        "learning_rate": round(lr, 6),
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "train_loss": round(loss * 1.1, 4),
            "val_loss": round(loss, 4),
            "train_acc": round(accuracy * 0.95, 4),
            "val_acc": round(accuracy, 4),
            "additional_metrics": {
                "precision": round(random.uniform(0.7, 0.9), 4),
                "recall": round(random.uniform(0.6, 0.85), 4),
                "f1_score": round(random.uniform(0.65, 0.88), 4),
                "auc": round(random.uniform(0.75, 0.95), 4),
            },
        },
        "hyperparameters": {
            "batch_size": random.choice([32, 64, 128]),
            "optimizer": random.choice(["adam", "sgd", "rmsprop"]),
            "momentum": round(random.uniform(0.8, 0.99), 2),
            "weight_decay": round(random.uniform(0.0001, 0.001), 6),
        },
        "environment": {
            "gpu": random.choice(
                ["NVIDIA GTX 1080", "NVIDIA RTX 2080", "NVIDIA RTX 3080"]
            ),
            "cpu_cores": random.choice([4, 8, 16]),
            "ram_gb": random.choice([16, 32, 64]),
            "os": random.choice(["Ubuntu 20.04", "Windows 10", "macOS Big Sur"]),
        },
        "experiment_details": {
            "experiment_id": f"exp_{random.randint(1000, 9999)}",
            "run_id": f"run_{random.randint(10000, 99999)}",
            "description": "Training run with enhanced metrics and hyperparameters",
            "start_time": datetime.now().isoformat(),
            "end_time": (
                datetime.now() + timedelta(hours=random.uniform(1, 3))
            ).isoformat(),
        },
    }


def simulate_random_error(
    iteration: int, max_iterations: int, error_type: str = "training"
):
    """
    Simulate a random error with stacktrace (non-blocking).

    Args:
        iteration: Current iteration number
        max_iterations: Total number of iterations
        error_type: Type of error context
    """
    # 5% chance of error
    if random.random() < 0.05:
        error_messages = [
            f"CUDA out of memory at iteration {iteration}",
            "DataLoader worker process crashed",
            "Gradient computation failed",
            "Model checkpoint save failed",
            "Validation data corrupted",
            "Learning rate scheduler error",
            "Model state dict mismatch",
            "Tensor dimension mismatch",
            "Optimizer step failed",
            "Loss computation error",
        ]

        error_msg = random.choice(error_messages)

        # Log with loguru (this will be captured by the logger)
        logger.warning(f"Non-critical {error_type} warning: {error_msg}")
        logger.debug(
            f"Error details: iteration={iteration}/{max_iterations}, context={error_type}"
        )

        # Sometimes add a more detailed error with stacktrace
        if random.random() < 0.3:
            try:
                # Simulate an exception
                raise ValueError(
                    f"Simulated {error_type} error at iteration {iteration}: {error_msg}"
                )
            except Exception as e:
                logger.error(f"Detailed {error_type} error: {str(e)}")
                print(f"Stacktrace details:\n{traceback.format_exc()}")


async def run_simulation(
    iterations: int, run_number: int = 1, use_payload_file: bool = False
):
    """
    Simulate either ML training or data processing with realistic logging.

    Args:
        iterations: Number of iterations (epochs for training, batches for processing)
        run_number: The run number for identification
        use_payload_file: If True, use payload.json file instead of generated metrics
    """
    config = {
        "title": "ML Training Simulation",
        "entity": "research-team",
        "name_prefix": "ml-training-run",
        "description_prefix": "Machine learning training simulation run",
        "config": {
            "model_type": "transformer",
            "dataset": "imagenet",
            "batch_size": 32,
            "learning_rate": 0.001,
            "epochs": iterations,
        },
        "progress_interval": 10,
        "debug_interval": 5,
    }

    # Load payload from file if requested
    payload_data = None
    if use_payload_file:
        try:
            with open("payload.json", "r") as f:
                payload_data = json.load(f)
            logger.info("Loaded payload data from payload.json file")
        except Exception as e:
            logger.error(f"Failed to load payload.json: {e}")
            logger.info("Falling back to generated training metrics")
            use_payload_file = False

    print(f"\n{'=' * 60}")
    print(f"Starting {config['title']} Run #{run_number}")
    print(f"{'Epochs training'}: {iterations}")
    print(f"{'Using payload file'}: {use_payload_file}")
    print(f"{'=' * 60}")

    # Initialize logger (no API key needed)
    mcl_client = mc.AsyncLoggerClient(app_name="examples/logger_example")
    mc_logger = mcl_client.logger

    try:
        # Initialize the logger
        logger.info(
            f"Starting simulation run #{run_number} with {iterations} iterations"
        )

        run = await mc_logger.init(
            project="data-universe-validators",
            entity=config["entity"],
            tags=[f"example-run-{run_number}"],
            notes=f"{config['title']} run #{run_number} with {iterations} iterations",
            config={
                **config["config"],
                "run_number": run_number,
                "use_payload_file": use_payload_file,
            },
            name=f"{config['name_prefix']}-{run_number}",
            description=f"{config['description_prefix']} #{run_number}",
        )
        print("🚀 Logger capturing started")

        logger.success(f"Logger initialized successfully with run ID: {run.id}")

        # Simulation loop
        start_time = time.time()

        for iteration in range(1, iterations + 1):
            # Simulate random errors (non-blocking)
            simulate_random_error(iteration, iterations)

            # Generate metrics based on simulation type or use payload data
            if use_payload_file and payload_data:
                # Use payload data from file, potentially cycling through if iterations > payload length
                if isinstance(payload_data, list):
                    payload_index = (iteration - 1) % len(payload_data)
                    metrics = payload_data[payload_index]
                    # Add iteration info to the payload
                    if isinstance(metrics, dict):
                        metrics["iteration"] = iteration
                        metrics["total_iterations"] = iterations
                else:
                    # If payload is not a list, use it directly
                    metrics = (
                        payload_data.copy()
                        if isinstance(payload_data, dict)
                        else {"data": payload_data}
                    )
                    metrics["iteration"] = iteration
                    metrics["total_iterations"] = iterations
            else:
                metrics = generate_training_metrics(iteration, iterations)

            # Log the metrics
            await mc_logger.log(metrics)

            # Log progress at specified intervals
            if iteration % config["progress_interval"] == 0 or iteration == iterations:
                if use_payload_file and payload_data:
                    logger.info(
                        f"Processing progress: Iteration {iteration}/{iterations} - Using payload data"
                    )
                else:
                    logger.info(
                        f"Training progress: Epoch {iteration}/{iterations} - Loss: {metrics['loss']:.4f}, "
                        f"Accuracy: {metrics['accuracy']:.4f}, LR: {metrics['learning_rate']:.6f}"
                    )

            # Additional debug logs
            if iteration % config["debug_interval"] == 0:
                logger.debug(f"Iteration {iteration} metrics: {metrics}")

            # Small delay to simulate processing time
            await asyncio.sleep(0.01)

        simulation_time = time.time() - start_time

        # Log final summary based on simulation type
        if use_payload_file and payload_data:
            final_metrics = {
                "processing_completed": True,
                "total_iterations": iterations,
                "processing_time_seconds": round(simulation_time, 2),
                "iterations_per_second": round(iterations / simulation_time, 2),
                "completed_at": datetime.now().isoformat(),
                "data_source": "payload.json",
            }
            success_message = (
                f"Processing completed successfully in {simulation_time:.2f} seconds - "
                f"Processed {iterations} iterations using payload data"
            )
        else:
            final_metrics = {
                "training_completed": True,
                "total_epochs": iterations,
                "final_loss": metrics["loss"],
                "final_accuracy": metrics["accuracy"],
                "training_time_seconds": round(simulation_time, 2),
                "epochs_per_second": round(iterations / simulation_time, 2),
                "completed_at": datetime.now().isoformat(),
            }
            success_message = (
                f"Training completed successfully in {simulation_time:.2f} seconds - "
                f"Final metrics: Loss={metrics['loss']:.4f}, Accuracy={metrics['accuracy']:.4f}"
            )

        await mc_logger.log(final_metrics)
        logger.success(success_message)

        return run.id

    except Exception as e:
        logger.error(f"Critical error in simulation run #{run_number}: {str(e)}")
        print(f"Stacktrace details:\n{traceback.format_exc()}")
        raise
    finally:
        logger.info(f"Finishing simulation run #{run_number}")
        print("🏁 Logger capturing finished")
        await mc_logger.finish()


async def main():
    """Main function to run the logger simulations."""
    start_time = time.time()
    print("🚀 Starting Logger Simulation Examples")
    print("This example demonstrates logger usage patterns:")

    try:
        run_id = await run_simulation(10, use_payload_file=True)
        print("\n🎉 All logger simulations completed successfully!")
        print(f"Run ID: {run_id}")
        print(
            "\nCheck the generated log files in your temp directory for the logged data."
        )

    except KeyboardInterrupt:
        print("Simulation interrupted by user")
    except Exception as e:
        print(f"Simulation failed with error: {str(e)}")
        print(f"Stacktrace details:\n{traceback.format_exc()}")
        raise
    finally:
        print(f"\nTotal time: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
