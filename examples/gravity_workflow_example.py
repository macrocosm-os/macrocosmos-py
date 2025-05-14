"""
Example of a complete Gravity workflow using the Macrocosmos SDK:
1. Check if a GravityTask exists and cancel it if found
2. Create a new task with multiple crawlers
3. Monitor data collection progress
4. Build datasets for crawlers with data
5. Monitor dataset build progress
6. Display dataset URLs and handle cleanup
"""

import asyncio
import os
import signal
import time
from typing import List, Set

import macrocosmos as mc
from macrocosmos.generated.gravity.v1 import gravity_pb2


class GravityWorkflow:
    def __init__(
        self,
        task_name: str,
        email: str,
        reddit_subreddit: str,
        x_hashtag: str,
        max_rows: int,
    ):
        self.task_name = task_name
        self.email = email
        self.reddit_subreddit = reddit_subreddit
        self.x_hashtag = x_hashtag
        self.max_rows = max_rows
        self.api_key = os.environ.get(
            "GRAVITY_API_KEY", os.environ.get("MACROCOSMOS_API_KEY")
        )
        self.client = mc.AsyncGravityClient(
            max_retries=1,
            timeout=30,
            api_key=self.api_key,
            app_name="examples/gravity_workflow_example",
        )
        self.task_id = None
        self.crawler_ids = []
        self.dataset_ids = []

    async def run(self):
        """Run the complete workflow."""
        try:
            # Step 1: Check if task exists and cancel it
            await self.find_and_cancel_existing_task()

            # Step 2: Create new task with X and Reddit crawlers
            await self.create_new_task()

            if not self.task_id:
                print("Failed to create task. Exiting.")
                return

            # Step 3: Monitor data collection progress
            crawlers_with_data = await self.monitor_data_collection()

            # Step 4: Build datasets for crawlers with data
            if crawlers_with_data:
                await self.build_datasets(crawlers_with_data)

                # Step 5 & 6: Monitor dataset builds and display URLs
                if self.dataset_ids:
                    await self.monitor_dataset_builds()

                    # Step 7: Wait for user input before cleanup
                    print(
                        "\n📌 Press Enter when you're done downloading the datasets to clean up and exit..."
                    )
                    # This runs in the background to allow the keyboard interrupt to work
                    await self.wait_for_input()
            else:
                print("\n⚠️ No crawlers collected data within the time limit.")
                await self.cleanup(self.task_id)

        except (KeyboardInterrupt, asyncio.CancelledError):
            print("\n⚠️ Operation canceled.")
            await self.cleanup(self.task_id)
        except Exception as e:
            print(f"\n❌ Error in workflow: {e}")
            await self.cleanup(self.task_id)
            raise

    async def find_and_cancel_existing_task(self):
        """Find and cancel any existing tasks with the given name that aren't completed."""
        print(f"\n🔍 Checking if tasks with name '{self.task_name}' exist...")

        try:
            # Get all tasks
            response = await self.client.gravity.GetGravityTasks(include_crawlers=False)

            existing_tasks: List[gravity_pb2.GravityTaskState] = []
            if response and response.gravity_task_states:
                for task in response.gravity_task_states:
                    if task.name == self.task_name:
                        existing_tasks.append(task)

            if existing_tasks:
                print(
                    f" Found {len(existing_tasks)} tasks with name '{self.task_name}'"
                )

                # Filter out completed tasks
                tasks_to_cancel = [
                    task for task in existing_tasks if task.status != "Completed"
                ]

                if tasks_to_cancel:
                    print(f" Cancelling {len(tasks_to_cancel)} non-completed tasks...")

                    for task in tasks_to_cancel:
                        await self.cleanup(task.gravity_task_id)

                    print("✅ All non-completed tasks cancelled successfully.")
                    # Wait a moment to ensure the cancellations are processed
                    await asyncio.sleep(3)
                else:
                    print("✅ All existing tasks are already completed.")
            else:
                print(f"✅ No existing tasks named '{self.task_name}' found.")

        except Exception as e:
            print(f"❌ Error checking/cancelling existing tasks: {e}")
            raise

    async def create_new_task(self):
        """Create a new task with X and Reddit crawlers."""
        print(f"\n🔨 Creating new task '{self.task_name}'...")

        try:
            # Define the crawlers
            gravity_tasks = [
                {"topic": self.x_hashtag, "platform": "x"},
                {"topic": self.reddit_subreddit, "platform": "reddit"},
            ]

            # User info for notifications
            notification = {
                "type": "email",
                "address": self.email,
                "redirect_url": "https://app.macrocosmos.ai/",
            }

            # Create the task
            response = await self.client.gravity.CreateGravityTask(
                gravity_tasks=gravity_tasks,
                name=self.task_name,
                notification_requests=[notification],
            )

            self.task_id = response.gravity_task_id
            print(f"✅ Task created successfully with ID: {self.task_id}")

            # Wait a moment to ensure the task is created
            await asyncio.sleep(10)

        except Exception as e:
            print(f"❌ Error creating new task: {e}")
            raise

    async def monitor_data_collection(self) -> Set[str]:
        """Monitor data collection for 60 seconds, return crawler IDs with data."""
        print("\n⏱️ Monitoring data collection for 60 seconds...")

        crawlers_with_data = set()
        start_time = time.time()
        end_time = start_time + 60  # 60 seconds time limit

        # First get the crawler IDs from the task
        try:
            response = await self.client.gravity.GetGravityTasks(
                gravity_task_id=self.task_id, include_crawlers=False
            )
            if response and response.gravity_task_states:
                task = response.gravity_task_states[0]
                self.crawler_ids = list(task.crawler_ids)
            else:
                print("❌ Gravity task response is empty")
                return crawlers_with_data
        except Exception as e:
            print(f"❌ Error getting crawler IDs: {e}")
            return crawlers_with_data

        # Display header
        print(
            "\n{:<12} {:<25} {:<15} {:<15}".format(
                "TIME", "CRAWLER", "STATUS", "RECORDS"
            )
        )
        print("─" * 70)
        print("\n")  # add a new line to be overwritten

        # Store the number of lines we need to clear
        num_status_lines = len(self.crawler_ids)

        while time.time() < end_time:
            elapsed = time.time() - start_time

            try:
                # Move cursor up to clear previous lines
                print(f"\033[{num_status_lines}A", end="")

                # Get status for each crawler
                for crawler_id in self.crawler_ids:
                    response = await self.client.gravity.GetCrawler(
                        crawler_id=crawler_id
                    )
                    if response and response.crawler:
                        crawler = response.crawler

                        # Check if this crawler has collected data
                        if crawler.state.records_collected > 0:
                            crawlers_with_data.add(crawler.crawler_id)

                        # Print status with color indicators
                        status_indicator = "⏳"
                        if crawler.state.status == "Running":
                            status_indicator = "🟢"
                        elif crawler.state.status == "Completed":
                            status_indicator = "✅"
                        elif crawler.state.status in ["Failed", "Cancelled"]:
                            status_indicator = "❌"

                        records = crawler.state.records_collected
                        records_display = (
                            f"{records} ↑" if records > 0 else str(records)
                        )

                        print(
                            "{:<12} {:<25} {:<15} {:<15}".format(
                                f"{elapsed:.1f}s",
                                f"{crawler.criteria.platform}/{crawler.criteria.topic}",
                                f"{status_indicator} {crawler.state.status}",
                                records_display,
                            )
                        )

                # Sleep for 10 seconds
                await asyncio.sleep(10)

            except Exception as e:
                print(f"❌ Error monitoring task: {e}")

        print(
            f"\n✅ Monitoring complete. Found {len(crawlers_with_data)} crawlers with data."
        )
        return crawlers_with_data

    async def build_datasets(self, crawler_ids: Set[str]):
        """Build datasets for crawlers that have collected data."""
        print(f"\n📦 Building datasets for {len(crawler_ids)} crawlers...")

        for crawler_id in crawler_ids:
            try:
                # Notification for dataset completion
                notification = {
                    "type": "email",
                    "address": self.email,
                    "redirect_url": "https://app.macrocosmos.ai/gravity/tasks",
                }

                # Build dataset
                response = await self.client.gravity.BuildDataset(
                    crawler_id=crawler_id,
                    max_rows=self.max_rows,
                    notification_requests=[notification],
                )

                if response and response.dataset_id:
                    self.dataset_ids.append(response.dataset_id)
                    print(f"✅ Dataset build initiated for crawler {crawler_id}")
                    print(f"   Dataset ID: {response.dataset_id}")
                else:
                    print(
                        f"❌ Failed to initiate dataset build for crawler {crawler_id}"
                    )

            except Exception as e:
                print(f"❌ Error building dataset for crawler {crawler_id}: {e}")
                raise

    async def monitor_dataset_builds(self):
        """Monitor the progress of dataset builds."""
        print(f"\n⏱️ Monitoring {len(self.dataset_ids)} dataset builds...")

        # Track which datasets are complete
        completed_datasets = set()
        dataset_status = {}  # Store current status for each dataset
        start_time = time.time()

        # Display header
        print(
            "\n{:<10} {:<25} {:<16} {:<12} {:<10} {:<30}".format(
                "TIME", "DATASET", "STATUS", "STEP", "PROGRESS", "MESSAGE"
            )
        )
        print("─" * 110)
        print("\n")  # add 2 new lines to be overwritten.

        # Store the number of lines we need to clear
        num_status_lines = len(self.dataset_ids)

        while len(completed_datasets) < len(self.dataset_ids):
            # Check if it's time to update dataset info (every 5s)
            if int(time.time() - start_time) % 5 == 0:
                # Get fresh data every 5 seconds
                for dataset_id in self.dataset_ids:
                    if dataset_id in completed_datasets:
                        continue

                    try:
                        response = await self.client.gravity.GetDataset(
                            dataset_id=dataset_id
                        )

                        if response and response.dataset:
                            dataset = response.dataset

                            # Calculate progress
                            step_count = len(dataset.steps)
                            total_steps = (
                                dataset.total_steps or 1
                            )  # Avoid division by zero
                            current_step = (
                                dataset.steps[-1].step if step_count > 0 else 0
                            )

                            # Get current step progress percentage (0.0-1.0)
                            step_progress = (
                                dataset.steps[-1].progress if step_count > 0 else 0.0
                            )
                            progress_pct = f"{step_progress * 100:.1f}%"

                            # Format step info
                            step_info = f"Step {current_step}/{total_steps}"

                            # Status indicator
                            status_indicator = "⏳"
                            if dataset.status == "Completed":
                                status_indicator = "✅"
                            elif dataset.status in ["Failed", "Cancelled"]:
                                status_indicator = "❌"

                            status_text = f"{status_indicator} {dataset.status}"
                            message = dataset.status_message or ""

                            # Store current status
                            dataset_status[dataset_id] = {
                                "status": status_text,
                                "step": step_info,
                                "progress": progress_pct,
                                "message": message,
                                "completed": dataset.status
                                in ["Completed", "Failed", "Cancelled"],
                                "dataset": dataset,
                            }

                            # Check if dataset is complete
                            if dataset.status in ["Completed", "Failed", "Cancelled"]:
                                completed_datasets.add(dataset_id)

                    except Exception as e:
                        dataset_status[dataset_id] = {
                            "status": "❌ Error",
                            "step": "Unknown",
                            "progress": "0.0%",
                            "message": str(e),
                            "completed": False,
                            "dataset": None,
                        }

            # Display current status for all datasets with updated elapsed time (refreshes every 1s)
            elapsed = time.time() - start_time

            # Move cursor up to clear previous lines
            print(f"\033[{num_status_lines}A", end="")

            # Redraw all status lines
            for dataset_id in self.dataset_ids:
                if dataset_id in dataset_status:
                    status = dataset_status[dataset_id]
                    id_short = (
                        dataset_id[:21] + "..." if len(dataset_id) > 24 else dataset_id
                    )
                    msg_truncated = (
                        status["message"][:27] + "..."
                        if len(status["message"]) > 30
                        else status["message"]
                    )

                    print(
                        "{:<10} {:<25} {:<16} {:<12} {:<10} {:<30}".format(
                            f"{elapsed:.1f}s",
                            id_short,
                            status["status"],
                            status["step"],
                            status["progress"],
                            msg_truncated,
                        )
                    )

            # Wait for 1 second before refreshing display
            await asyncio.sleep(10)

            # If some datasets just completed, don't clear lines to preserve final status
            if len(completed_datasets) == len(self.dataset_ids):
                break

        # Show completed dataset files
        for dataset_id in self.dataset_ids:
            if (
                dataset_id in dataset_status
                and dataset_status[dataset_id]["completed"]
                and dataset_status[dataset_id]["dataset"]
            ):
                dataset = dataset_status[dataset_id]["dataset"]

                if dataset.status == "Completed" and dataset.files:
                    print(f"\n📄 Dataset {dataset_id} files available:")
                    for i, file in enumerate(dataset.files):
                        file_size_mb = file.file_size_bytes / (1024 * 1024)
                        print(f"   File {i + 1}: {file.file_name}")
                        print(f"   • Size: {file_size_mb:.2f} MB")
                        print(f"   • Rows: {file.num_rows}")
                        print(f"   • URL: {file.url}")

        print("\n✅ All dataset builds completed!")

    async def wait_for_input(self):
        """Wait for user input in a non-blocking way."""
        # Using run_in_executor to run synchronous input() in a thread pool
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, input)
        await self.cleanup(self.task_id)

    async def cleanup(self, task_id: str):
        """Cancel the task and cleanup resources."""
        print("\n🧹 Cleaning up:")
        if task_id:
            try:
                print(f"  • Cancelling gravity task {task_id}...")
                await self.client.gravity.CancelGravityTask(gravity_task_id=task_id)
            except Exception as e:
                print(f"❌ Error cancelling task: {e}")
        if self.dataset_ids:
            for dataset_id in self.dataset_ids:
                try:
                    print(f"  • Cancelling dataset {dataset_id}...")
                    await self.client.gravity.CancelDataset(dataset_id=dataset_id)
                except Exception:
                    continue


def get_user_input():
    """Get user input with defaults."""
    print("\n📝 Please enter your preferences (press Enter for defaults):")

    # Get email with default
    email = input("Email address [your@email.com]: ").strip()
    if not email:
        email = "your@email.com"

    # Get Reddit subreddit with default
    reddit = input("Reddit subreddit [r/MachineLearning]: ").strip()
    if not reddit:
        reddit = "r/MachineLearning"
    elif not reddit.startswith("r/"):
        reddit = f"r/{reddit}"

    # Get X hashtag with default
    x_hashtag = input("X hashtag [#ai]: ").strip()
    if not x_hashtag:
        x_hashtag = "#ai"
    elif not x_hashtag.startswith("#"):
        x_hashtag = f"#{x_hashtag}"

    # Get task name with default
    task_name = input("Task name [MyTestTask]: ").strip()
    if not task_name:
        task_name = "MyTestTask"

    # Get max rows with default
    while True:
        max_rows_input = input("Max rows per dataset [1000]: ").strip()
        if not max_rows_input:
            max_rows = 1000
            break
        try:
            max_rows = int(max_rows_input)
            if max_rows <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    return email, reddit, x_hashtag, task_name, max_rows


async def main():
    print("════════════════════════════════════════════════════")
    print("          🚀 Gravity Workflow Example")
    print("════════════════════════════════════════════════════")

    # Get user input with defaults
    email, reddit, x_hashtag, task_name, max_rows = get_user_input()

    # Set up signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()

    workflow = GravityWorkflow(task_name, email, reddit, x_hashtag, max_rows)

    # Register signal handlers
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda: asyncio.create_task(handle_signal(workflow))
        )

    print("\n▶️ Starting workflow...")
    await workflow.run()


async def handle_signal(workflow):
    """Handle termination signals by cleaning up."""
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():  # Don't cancel our signal handler
            task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
