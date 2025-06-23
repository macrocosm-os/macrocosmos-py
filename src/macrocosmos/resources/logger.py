import asyncio
import json
import os
import random
import string
import tempfile
import threading
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
from macrocosmos.resources.logging.console_handler import ConsoleCapture
from macrocosmos.resources.logging.request import make_request


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
        self._temp_dir: Optional[Path] = None
        self._file_manager: Optional[FileManager] = None
        self._upload_thread: Optional[threading.Thread] = None
        self._stop_upload: Optional[threading.Event] = None
        self._upload_worker: Optional[UploadWorker] = None

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
    ) -> str:
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
        )

        # Create temporary directory
        self._temp_dir = Path(tempfile.gettempdir()) / f"mcl_run_{self._run.run_id}"
        self._temp_dir.mkdir(exist_ok=True)

        # Handle startup recovery - send any existing files asynchronously
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._handle_startup_recovery, self._temp_dir)

        # Create file manager
        self._file_manager = FileManager(self._temp_dir, self._run)

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

        # Start upload thread
        self._stop_upload = threading.Event()
        self._upload_worker = UploadWorker(
            self._file_manager, self._client, self._stop_upload
        )
        self._upload_thread = threading.Thread(
            target=self._upload_worker.upload_worker, daemon=True
        )
        self._upload_thread.start()

        return self._run.run_id

    async def log(self, data: Dict[str, Any]) -> None:
        """
        Log data to the run.

        Args:
            data: The data to log.
            step: The step number (optional).
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
            None,
            self._file_manager.get_file(FileType.HISTORY).write,
            json.dumps(record) + "\n",
        )

    async def finish(self) -> None:
        """
        Finish the logging run and cleanup resources.
        """
        if not self._run:
            return

        # Stop upload thread
        if hasattr(self, "_stop_upload") and self._stop_upload is not None:
            self._stop_upload.set()
            if self._upload_thread and self._upload_thread.is_alive():
                self._upload_thread.join(timeout=5)

        # Stop logging capture
        if self._console_capture:
            self._console_capture.stop_capture()

        # Send any remaining data
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_remaining_data)

        # Cleanup
        self._run = None
        self._console_capture = None
        self._temp_dir = None
        self._file_manager = None
        self._upload_thread = None
        self._upload_worker = None
        self._stop_upload = None

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

        await make_request(self._client, "CreateRun", request)

    def _send_remaining_data(self) -> None:
        """Send any remaining data in files."""
        if self._temp_dir and self._temp_dir.exists():
            for file_type in FILE_MAP.keys():
                file_obj = self._file_manager.get_file(file_type)
                with file_obj.lock:
                    if file_obj.exists():
                        self._upload_worker._send_file_data(file_obj)

    def _handle_startup_recovery(self, skip_dir: Optional[Path] = None) -> None:
        """Handle startup recovery by sending any existing files from previous runs, except the specified skip directory."""
        temp_dir = Path(tempfile.gettempdir())

        # Search for any existing mcl_run_* directories
        for run_dir in temp_dir.glob("mcl_run_*"):
            if run_dir.is_dir() and run_dir != skip_dir:
                # For recovery, we don't need run info since we're just reading existing files
                tmp_file_manager = FileManager(run_dir)
                # Create a temporary stop event for recovery upload worker
                tmp_stop_event = threading.Event()
                tmp_upload_worker = UploadWorker(
                    tmp_file_manager, self._client, tmp_stop_event
                )
                for file_type in FILE_MAP.keys():
                    file_obj = tmp_file_manager.get_file(file_type)
                    with file_obj.lock:
                        if file_obj.exists():
                            tmp_upload_worker._send_file_data(file_obj)

                    tmp_file_path = file_obj.path.with_suffix(
                        file_obj.path.suffix + TEMP_FILE_SUFFIX
                    )
                    tmp_file_obj = File(tmp_file_path, file_type)
                    with tmp_file_obj.lock:
                        if tmp_file_obj.exists():
                            tmp_upload_worker._send_file_data(
                                tmp_file_obj, tmp_file_path
                            )


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
        return asyncio.run(
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

    def log(self, data: Dict[str, Any], step: Optional[int] = None) -> None:
        """
        Log data to the run synchronously.

        Args:
            data: The data to log.
            step: The step number (optional).
        """
        asyncio.run(self._async_logger.log(data=data, step=step))

    def finish(self) -> None:
        """
        Finish the logging run and cleanup resources synchronously.
        """
        asyncio.run(self._async_logger.finish())
