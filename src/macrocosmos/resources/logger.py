import asyncio
import concurrent.futures
import json
import os
import random
import string
import signal
import tempfile
import threading
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.logger.v1 import logger_pb2
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources.logging.file_manager import (
    FileType,
    FileManager,
    File,
    FILE_MAP,
    TEMP_FILE_SUFFIX,
)
from macrocosmos.resources.logging.run import Run
from macrocosmos.resources.logging.upload_worker import UploadWorker
from macrocosmos.resources.logging.file_monitor import FileMonitor
from macrocosmos.resources.logging.console_handler import ConsoleCapture
from macrocosmos.resources.logging.request import make_async_request
from macrocosmos.resources._utils import run_sync_threadsafe

logger = logging.getLogger(__name__)


class AsyncLogger:
    """Asynchronous Logger resource for logging data to the Macrocosmos platform."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous Logger resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._run: Optional[Run] = None
        self._console_capture: Optional[ConsoleCapture] = None
        self._temp_dir = Path(tempfile.gettempdir())
        self._temp_run_dir: Optional[Path] = None
        self._file_manager: Optional[FileManager] = None
        self._stop_monitoring: Optional[threading.Event] = None
        self._file_monitor: Optional[FileMonitor] = None
        self._stop_upload: Optional[threading.Event] = threading.Event()
        self._upload_worker: UploadWorker = UploadWorker(
            self._client, self._stop_upload
        )

        # Create thread pool for upload operations
        self._thread_pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=10,
            thread_name_prefix="mcl_logger_thread_pool",
        )

        # Cleanup state tracking
        self._cleanup_lock = threading.Lock()
        self._is_cleaning_up = False
        self._cleanup_complete = threading.Event()

        # Set up signal handlers for graceful shutdown
        self._setup_signal_handlers()

        # Handle startup recovery - send any existing files asynchronously in background
        self._monitor_future: Optional[concurrent.futures.Future] = None
        self._recovery_future = self._thread_pool.submit(self._handle_startup_recovery)
        self._recovery_upload_futures: List[concurrent.futures.Future] = []
        self._monitor_upload_futures: List[concurrent.futures.Future] = []
        self._remaining_upload_futures: List[concurrent.futures.Future] = []

    async def init(
        self,
        project: str,
        entity: Optional[str] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        reinit: bool = False,
    ) -> Run:
        """
        Initialize a new logging run.

        Args:
            project: The project name.
            entity: The entity name (optional).
            tags: List of tags (optional).
            notes: Notes for the run (optional).
            config: Configuration dictionary (optional).
            name: Name of the run (optional).
            description: Description of the run (optional).
            reinit: Whether to reinitialize if already initialized (default: False).

        Returns:
            The run ID.
        """
        if self._run and not reinit:
            raise RuntimeError(
                "Logger already initialized. Use reinit=True to reinitialize."
            )

        if reinit:
            await self.finish()

        base_tags = [f"{__package_name__}/{__version__}"]
        if self._client.app_name:
            base_tags.append(self._client.app_name)

        run_id = self._generate_run_id()
        self._run = Run(
            run_id=run_id,
            project=project,
            entity=entity or "macrocosmos",
            name=name or f"run-{run_id}",
            description=description,
            notes=notes,
            tags=base_tags + (tags or []),
            config=config or {},
            start_time=datetime.now(),
            finish_callback=self.finish,
        )

        # Create temporary run directory
        self._temp_run_dir = self._temp_dir / f"mcl_run_{self._run.run_id}"
        self._temp_run_dir.mkdir(exist_ok=True)

        # Create file manager
        self._file_manager = FileManager(self._temp_run_dir, self._run)

        # Create run via gRPC
        await self._create_run()

        # Start logging capture if enabled
        if os.environ.get("MACROCOSMOS_CAPTURE_LOGS", "true").lower() in (
            "true",
            "1",
            "yes",
        ):
            self._console_capture = ConsoleCapture(
                self._file_manager.log_file, self._run
            )
            self._console_capture.start_capture()

        # Start file monitoring using thread pool
        self._stop_monitoring = threading.Event()
        self._file_monitor = FileMonitor(
            self._file_manager,
            self._stop_monitoring,
            upload_worker=self._upload_worker,
            thread_pool=self._thread_pool,
            upload_futures=self._monitor_upload_futures,
        )
        self._monitor_future = self._thread_pool.submit(
            self._file_monitor.monitor_files
        )

        return self._run

    async def log(self, data: Dict[str, Any]) -> None:
        """
        Log data to the run.

        Args:
            data: The data to log.
        """
        if not self._run:
            raise RuntimeError("Logger not initialized. Call init() first.")

        record = {
            "timestamp": datetime.now().isoformat(),
            "payload_json": json.dumps(data),
            "sequence": self._run.next_step(),
            "runtime": self._run.runtime,
        }

        # Write to history file
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            self._thread_pool,
            self._file_manager.get_file(FileType.HISTORY).write,
            json.dumps(record) + "\n",
        )

    async def finish(self) -> None:
        """
        Finish the logging run and cleanup resources.
        """
        if not self._run:
            return

        # Stop monitoring for this run
        if self._stop_monitoring is not None:
            self._stop_monitoring.set()
            if self._monitor_future and not self._monitor_future.done():
                try:
                    self._monitor_future.result(timeout=1)
                except concurrent.futures.TimeoutError:
                    logger.warning("monitor future timed out")
                    pass  # Monitor thread will be cleaned up with thread pool

        # Stop logging capture
        if self._console_capture:
            self._console_capture.stop_capture()

        # Wait for all monitor upload futures to complete before sending remaining data
        if self._monitor_upload_futures:
            # Create a copy of the list to avoid modification during iteration
            futures_to_wait = list(self._monitor_upload_futures)
            for future in futures_to_wait:
                try:
                    if not future.done():
                        await asyncio.wrap_future(future)
                except Exception:
                    # Log or handle exceptions from upload failures
                    pass

        # Send any remaining data using thread pool
        # We need to wait for the monitor_upload_futures to complete so that we don't conflict with its uploads
        if self._thread_pool:
            future = self._thread_pool.submit(
                self._send_remaining_data, Path(self._temp_run_dir)
            )
            await asyncio.wrap_future(future)

        # Clear monitor upload futures after processing
        if self._monitor_upload_futures:
            self._monitor_upload_futures.clear()

        # Cleanup run-specific resources
        self._run = None
        self._console_capture = None
        self._temp_run_dir = None
        self._file_manager = None
        self._monitor_future = None
        self._file_monitor = None
        self._stop_monitoring = None

    def __del__(self):
        """Cleanup when object is destroyed. This is a fallback for when signal handlers aren't triggered."""
        self._cleanup()

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown on keyboard interrupt."""

        def signal_handler(signum, frame):
            """Handle termination signals by setting stop events."""
            self._cleanup()

        # Register signal handlers for common termination signals
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # Termination signal

        # On Windows, also handle SIGBREAK
        if hasattr(signal, "SIGBREAK"):
            signal.signal(signal.SIGBREAK, signal_handler)

    def _cleanup(self) -> None:
        """
        Ensure complete cleanup happens exactly once (finish current run + global cleanup).
        This method is thread-safe and idempotent.
        """
        with self._cleanup_lock:
            if self._is_cleaning_up:
                # Already cleaning up, wait for completion
                self._cleanup_complete.wait(timeout=10)
                return

            self._is_cleaning_up = True

        try:
            # First, finish the current run if there is one
            if self._run is not None:
                try:
                    # Try to finish the run asynchronously if we're in an async context
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Create a task to finish the logger asynchronously
                        asyncio.create_task(self.finish())
                    else:
                        # No event loop running, do best-effort cleanup
                        raise RuntimeError("no event loop")
                except Exception:
                    # No event loop running, do best-effort cleanup
                    if self._run:
                        # Stop monitoring for this run
                        if self._stop_monitoring is not None:
                            self._stop_monitoring.set()

                        # Stop logging capture
                        if self._console_capture:
                            self._console_capture.stop_capture()

            # Then, ensure global cleanup (stop uploads, shutdown thread pool)
            self._stop_upload.set()

            # Wait for recovery futures to complete (if still running)
            if self._recovery_upload_futures:
                for future in self._recovery_upload_futures:
                    try:
                        if not future.done():
                            future.result(timeout=1)
                    except concurrent.futures.TimeoutError:
                        logger.warning("recovery upload future timed out")
                        pass  # Recovery thread will be cleaned up with thread pool

            # Wait for recovery thread to complete (if still running)
            if self._recovery_future and not self._recovery_future.done():
                try:
                    self._recovery_future.result(timeout=1)
                except concurrent.futures.TimeoutError:
                    logger.warning("recovery future timed out")
                    pass  # Recovery thread will be cleaned up with thread pool

            # Wait for remaining upload futures to complete (if still running)
            if self._remaining_upload_futures:
                for future in self._remaining_upload_futures:
                    try:
                        if not future.done():
                            future.result(timeout=1)
                    except concurrent.futures.TimeoutError:
                        logger.warning("remaining upload future timed out")
                        pass  # Remaining upload thread will be cleaned up with thread pool

            # Shutdown thread pool
            if hasattr(self, "_thread_pool") and self._thread_pool:
                self._thread_pool.shutdown(wait=True, cancel_futures=True)
        finally:
            self._cleanup_complete.set()

    def _generate_run_id(self) -> str:
        """
        Generate a unique run ID using epoch time in base-36 plus 3 random alphanumeric characters.

        Returns:
            A unique run ID string.
        """
        # Get current epoch time and convert to base-36
        epoch_time = int(time.time())
        epoch_base36 = ""
        while epoch_time > 0:
            epoch_time, remainder = divmod(epoch_time, 36)
            if remainder < 10:
                epoch_base36 = chr(48 + remainder) + epoch_base36  # 48 is ASCII for '0'
            else:
                epoch_base36 = (
                    chr(87 + remainder) + epoch_base36
                )  # 87 is ASCII for 'a' - 10

        # Generate 3 random alphanumeric characters
        random_suffix = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=3)
        )

        return f"{epoch_base36}{random_suffix}"

    async def _create_run(self) -> None:
        """Create a new run via gRPC."""
        request = logger_pb2.CreateRunRequest(
            run_id=self._run.run_id,
            name=self._run.name,
            project=self._run.project,
            tags=self._run.tags,
            config_json=json.dumps(self._run.config),
            created_at=self._run.start_time,
            description=self._run.description,
            notes=self._run.notes,
            entity=self._run.entity,
        )

        await make_async_request(self._client, "CreateRun", request)

    def _send_remaining_data(self, temp_dir: Path) -> None:
        """Send any remaining data in files using thread pool."""
        if (
            temp_dir
            and temp_dir.exists()
            and self._thread_pool
            and not self._stop_upload.is_set()
        ):
            file_manager = FileManager(temp_dir)
            for file_type in FILE_MAP.keys():
                file_obj = file_manager.get_file(file_type)
                with file_obj.lock:
                    if file_obj.exists():
                        future = self._thread_pool.submit(
                            self._upload_worker.upload_file, file_obj
                        )
                        self._remaining_upload_futures.append(future)

    def _handle_startup_recovery(self) -> None:
        """
        Handle startup recovery by sending any existing files from previous runs.

        This method runs asynchronously in a background thread and does not block the initialization
        of new logging runs. It searches for orphaned log files from previous runs and uploads them
        to ensure no data is lost.
        """
        thread_pool = self._thread_pool
        temp_dir = self._temp_dir

        # Search for any existing mcl_run_* directories
        run_dirs = [
            run_dir for run_dir in temp_dir.glob("mcl_run_*") if run_dir.is_dir()
        ]
        blocking_temp_uploads = dict()

        for f in ["temp", "regular"]:
            for run_dir in run_dirs:
                # For recovery, we don't need run info since we're just reading existing files
                tmp_file_manager = FileManager(run_dir)

                # Check for files and submit upload tasks to thread pool
                for file_type in FILE_MAP.keys():
                    file_obj = tmp_file_manager.get_file(file_type)
                    tmp_file_path = None
                    key = (run_dir, file_type)

                    if f == "temp":
                        tmp_file_path = file_obj.path.with_suffix(
                            file_obj.path.suffix + TEMP_FILE_SUFFIX
                        )
                        file_obj = File(tmp_file_path, file_type)
                    else:
                        # check if we have blocking temp upload matching this regular file
                        if key in blocking_temp_uploads:
                            if file_obj.exists():
                                # we will skip this for now and we will upload it once the temp file is done
                                continue
                            else:
                                # we don't need to monitor this temp file upload - proceed with upload
                                del blocking_temp_uploads[key]

                    with file_obj.lock:
                        if file_obj.exists():
                            future = thread_pool.submit(
                                self._upload_worker.upload_file,
                                file_obj,
                                tmp_file_path,
                            )
                            self._recovery_upload_futures.append(future)
                            if f == "temp":
                                blocking_temp_uploads[key] = future

        # Process blocked regular files after temp files are done
        future_to_name = {
            future: name for name, future in blocking_temp_uploads.items()
        }
        for future in concurrent.futures.as_completed(future_to_name.keys()):
            name = future_to_name[future]
            run_dir, file_type = name
            tmp_file_manager = FileManager(run_dir)
            file_obj = tmp_file_manager.get_file(file_type)
            with file_obj.lock:
                if file_obj.exists():
                    future = thread_pool.submit(
                        self._upload_worker.upload_file,
                        file_obj,
                    )
                    self._recovery_upload_futures.append(future)

    @property
    def run(self) -> Optional[Run]:
        """Get the current run."""
        return self._run


class Logger:
    """Synchronous Logger resource for logging data to the Macrocosmos platform."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous Logger resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_logger = AsyncLogger(client)

    def init(
        self,
        project: str,
        entity: Optional[str] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        reinit: bool = False,
    ) -> str:
        """
        Initialize a new logging run synchronously.

        Args:
            project: The project name.
            entity: The entity name (optional).
            tags: List of tags (optional).
            notes: Notes for the run (optional).
            config: Configuration dictionary (optional).
            name: Name of the run (optional).
            description: Description of the run (optional).
            reinit: Whether to reinitialize if already initialized (default: False).

        Returns:
            The run ID.
        """
        return run_sync_threadsafe(
            self._async_logger.init(
                project=project,
                entity=entity,
                tags=tags,
                notes=notes,
                config=config,
                name=name,
                description=description,
                reinit=reinit,
            )
        )

    def log(self, data: Dict[str, Any]) -> None:
        """
        Log data to the run synchronously.

        Args:
            data: The data to log.
        """
        run_sync_threadsafe(self._async_logger.log(data=data))

    def finish(self) -> None:
        """
        Finish the logging run and cleanup resources synchronously.
        """
        run_sync_threadsafe(self._async_logger.finish())

    @property
    def run(self) -> Optional[Run]:
        """Get the current run."""
        return self._async_logger.run
