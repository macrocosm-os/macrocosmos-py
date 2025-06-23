"""
Example demonstrating the Logger functionality with realistic usage patterns.
This example creates two runs simulating actual application logging with predefined payload structures.
"""

import asyncio
import random
import time
import traceback
from datetime import datetime, timedelta
from typing import Dict, Any

import macrocosmos as mc
from loguru import logger


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


def generate_data_processing_metrics(
    batch: int, total_batches: int, data_type: str
) -> Dict[str, Any]:
    """
    Generate realistic data processing metrics.

    Args:
        batch: Current batch number
        total_batches: Total number of batches
        data_type: Type of data being processed

    Returns:
        Dictionary with processing metrics
    """
    progress = batch / total_batches

    # Simulate processing time and throughput
    base_time = 0.1 + 0.2 * random.random()
    throughput = 1000 + 500 * random.random()

    return {
        "batch": batch,
        "total_batches": total_batches,
        "data_type": data_type,
        "progress": progress,
        "processing_time": round(base_time, 3),
        "throughput": round(throughput, 0),
        "memory_usage": round(512 + 256 * random.random(), 0),
        "timestamp": datetime.now().isoformat(),
        "status": "completed" if batch == total_batches else "processing",
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


async def run_simulation(simulation_type: str, iterations: int, run_number: int = 1):
    """
    Simulate either ML training or data processing with realistic logging.

    Args:
        run_number: The run number for identification
        simulation_type: Type of simulation ("training" or "processing")
        iterations: Number of iterations (epochs for training, batches for processing)
    """
    simulation_config = {
        "training": {
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
        },
        "processing": {
            "title": "Data Processing Simulation",
            "entity": "data-team",
            "name_prefix": "data-processing-run",
            "description_prefix": "Data processing pipeline simulation run",
            "config": {
                "pipeline_type": "etl",
                "data_source": "database",
                "batch_size": 1000,
                "total_batches": iterations,
            },
            "progress_interval": 50,
            "debug_interval": 25,
        },
    }

    config = simulation_config[simulation_type]

    print(f"\n{'=' * 60}")
    print(f"Starting {config['title']} Run #{run_number}")
    print(f"{'Epochs' if simulation_type == 'training' else 'Batches'}: {iterations}")
    print(f"{'=' * 60}")

    # Initialize logger (no API key needed)
    mcl_client = mc.AsyncLoggerClient(app_name="examples/logger_example")
    mc_logger = mcl_client.logger

    try:
        # Initialize the logger
        logger.info(
            f"Starting {simulation_type} simulation run #{run_number} with {iterations} iterations"
        )

        run_id = await mc_logger.init(
            project="data-universe-validators",
            entity=config["entity"],
            tags=[f"example-run-{run_number}"],
            notes=f"{config['title']} run #{run_number} with {iterations} iterations",
            config={
                **config["config"],
                "run_number": run_number,
            },
            name=f"{config['name_prefix']}-{run_number}",
            description=f"{config['description_prefix']} #{run_number}",
        )

        logger.success(f"Logger initialized successfully with run ID: {run_id}")

        # Simulation loop
        start_time = time.time()

        for iteration in range(1, iterations + 1):
            # Simulate random errors (non-blocking)
            simulate_random_error(iteration, iterations, simulation_type)

            # Generate metrics based on simulation type
            if simulation_type == "training":
                metrics = generate_training_metrics(iteration, iterations)
            else:
                metrics = generate_data_processing_metrics(
                    iteration, iterations, "training_data"
                )

            # Log the metrics
            await mc_logger.log(metrics)

            # Log progress at specified intervals
            if iteration % config["progress_interval"] == 0 or iteration == iterations:
                if simulation_type == "training":
                    logger.info(
                        f"Training progress: Epoch {iteration}/{iterations} - Loss: {metrics['loss']:.4f}, "
                        f"Accuracy: {metrics['accuracy']:.4f}, LR: {metrics['learning_rate']:.6f}"
                    )
                else:
                    logger.info(
                        f"Processing progress: Batch {iteration}/{iterations} - "
                        f"Progress: {metrics['progress']:.1%}, "
                        f"Throughput: {metrics['throughput']:.0f} items/s, "
                        f"Memory: {metrics['memory_usage']:.0f}MB"
                    )

            # Additional debug logs
            if iteration % config["debug_interval"] == 0:
                logger.debug(f"Iteration {iteration} metrics: {metrics}")

            # Small delay to simulate processing time
            await asyncio.sleep(0.01)

        simulation_time = time.time() - start_time

        # Log final summary based on simulation type
        if simulation_type == "training":
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
        else:
            final_metrics = {
                "processing_completed": True,
                "total_batches": iterations,
                "total_items_processed": iterations * 1000,
                "processing_time_seconds": round(simulation_time, 2),
                "average_throughput": round((iterations * 1000) / simulation_time, 0),
                "completed_at": datetime.now().isoformat(),
            }
            success_message = (
                f"Data processing completed successfully in {simulation_time:.2f} seconds - "
                f"Processed {iterations * 1000:,} items at {final_metrics['average_throughput']:.0f} items/s"
            )

        await mc_logger.log(final_metrics)
        logger.success(success_message)

        return run_id

    except Exception as e:
        logger.error(f"Critical error in {simulation_type} run #{run_number}: {str(e)}")
        print(f"Stacktrace details:\n{traceback.format_exc()}")
        raise
    finally:
        logger.info(f"Finishing {simulation_type} run #{run_number}")
        await mc_logger.finish()


async def main():
    """Main function to run the logger simulations."""
    print("🚀 Starting Logger Simulation Examples")
    print("This example demonstrates realistic logger usage patterns:")
    print("  - Run 1: ML Training simulation (50 epochs)")
    print("  - Run 2: Data Processing simulation (200 batches)")

    try:
        run_id = await run_simulation(3, "training", 2000)
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


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
