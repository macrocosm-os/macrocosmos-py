# Logger
Logger is the Macrocosmos logging utility used by Macrocosmos subnets for capturing subnet node activity.


## Example usage
Here's a simple example of a `run` method that utlizes the Macrocosmos logger.
```py
import macrocosmos as mc
from loguru import logger

async def run():
    mcl_client = mc.AsyncLoggerClient(app_name="my_app")
    mc_logger = mcl_client.logger

    # Start a new run
    run = await mc_logger.init(
        project="data-universe-validators",
        tags=[f"example"],
        notes=f"Additional notes",
        config={"key": "value"},
        name=f"My Example",
        description=f"This is an example",
    )

    logger.success(f"🚀 Logger initialized successfully with run ID: {run.id}")

    try:
        while True:
            # Do something
            logger.info("Captured log message")

            # Log metrics
            metrics = {"key": "value"}
            await mc_logger.log(metrics)
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        raise
    finally:
        logger.info(f"🏁 Finished")
        await mc_logger.finish()  # or use `run.finish()`
```

## Disable Console Capture
All console messages (i.e. log messages) are automatically captured by `mc_logger` between the `init()` and `finish()` calls.  This can be disabled by setting the environment variable `MACROCOSMOS_CAPTURE_LOGS=false`.
