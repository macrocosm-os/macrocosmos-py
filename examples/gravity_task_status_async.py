"""
Example that demonstrates how to get the status of a specific gravity task using async/await.
"""

import asyncio
import os

import macrocosmos as mc


async def main():
    # Get API key from environment variable
    api_key = os.environ.get("GRAVITY_API_KEY", os.environ.get("MACROCOSMOS_API_KEY"))

    # Create an async Gravity client
    client = mc.AsyncGravityClient(
        max_retries=1,
        timeout=30,
        api_key=api_key,
        app_name="examples/gravity_task_status_async",
    )

    # Get gravity task ID from user
    task_id = input("Enter the gravity task ID: ").strip()

    try:
        # Get the task status
        response = await client.gravity.GetGravityTasks(
            gravity_task_id=task_id, include_crawlers=True
        )

        if not response.gravity_task_states:
            print(f"No task found with ID: {task_id}")
            return

        # Print task details
        task = response.gravity_task_states[0]
        print("\nTask Details:")
        print(f"ID: {task.gravity_task_id}")
        print(f"Name: {task.name}")
        print(f"Status: {task.status}")
        print(f"Start Time: {task.start_time}")
        print(f"Number of Crawlers: {len(task.crawler_ids)}")

        # Print crawler details if available
        if task.crawler_workflows:
            print("\nCrawler Details:")
            for crawler in task.crawler_workflows:
                print(f"\nCrawler ID: {crawler.crawler_id}")
                print(f"State: {crawler.state}")
                print(f"Start Time: {crawler.start_time}")
                if crawler.deregistration_time:
                    print(f"Deregistration Time: {crawler.deregistration_time}")
                if crawler.archive_time:
                    print(f"Archive Time: {crawler.archive_time}")

    except Exception as e:
        print(f"Error getting task status: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
