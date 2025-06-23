import asyncio
import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from google.protobuf import timestamp_pb2
from macrocosmos.generated.logger.v1 import logger_pb2
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources.logging.file_manager import (
    File,
    FileManager,
    FILE_MAP,
    TEMP_FILE_SUFFIX,
)
from macrocosmos.resources.logging.request import make_request

MAX_FILE_SIZE_MB = 5  # 5MB
MIN_FILE_AGE_SEC = 10  # 10 seconds


class UploadWorker:
    """Background worker for uploading log files to the server."""

    def __init__(
        self,
        file_manager: FileManager,
        client: BaseClient,
        stop_upload: threading.Event,
    ):
        """
        Initialize the logging worker.

        Args:
            file_manager: The file manager instance.
            client: The client instance for making requests.
            stop_upload: The stop event for the upload thread.
        """
        self.file_manager = file_manager
        self.client = client
        self._stop_upload = stop_upload

    def _should_upload_file(self, file_obj: File) -> bool:
        """Check if a file should be uploaded based on size and time."""
        # Note: This method is called while holding the file lock, so file existence
        # should be stable, but we still handle potential race conditions defensively

        try:
            if not file_obj.exists():
                return False

            # Get file stats once to avoid multiple stat calls
            stat_info = file_obj.path.stat()

            # Check file size (>5MB)
            if stat_info.st_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                return True

            # Check if there are records to upload (excluding header)
            if file_obj.has_records():
                # Check file age (>10s) using the stat info we already have
                file_age = time.time() - stat_info.st_mtime
                if file_age > MIN_FILE_AGE_SEC:
                    return True

            return False
        except (OSError, IOError):
            # File was deleted or became inaccessible between checks
            return False

    async def _send_file_data_async(
        self, file_obj: File, temp_file: Optional[Path] = None
    ) -> None:
        """Send file data to the server asynchronously."""
        # Read header to get run info
        header_data = file_obj.read_file_header()
        if not header_data:
            raise ValueError("run_id and project are required for sending file data")

        # If temp_file is provided, use it directly (for recovery of orphaned temp files)
        # Otherwise, check if there are records and rename the file
        if temp_file is None:
            temp_file = file_obj.path.with_suffix(
                file_obj.path.suffix + TEMP_FILE_SUFFIX
            )

            # Check if there are records before renaming
            with file_obj.lock:
                if not file_obj.has_records():
                    # No records, just clean up the file
                    if file_obj.path.exists():
                        file_obj.path.unlink()
                    return
                file_obj.path.rename(temp_file)

        # Using temp file, we don't need to lock the file since there will only be one upload worker
        try:
            records = []
            with open(temp_file, "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.strip():
                        try:
                            record_data = json.loads(line)

                            # Skip header row
                            if record_data.get("__type") == "header":
                                continue

                            # Convert datetime string to protobuf timestamp
                            dt = datetime.fromisoformat(record_data["timestamp"])
                            timestamp = timestamp_pb2.Timestamp()
                            timestamp.FromDatetime(dt)

                            record = logger_pb2.Record(
                                timestamp=timestamp,
                                payload_json=record_data["payload_json"],
                                payload_name=record_data.get("payload_name"),
                                sequence=record_data.get("sequence"),
                                runtime=record_data.get("runtime"),
                            )
                            records.append(record)
                        except (json.JSONDecodeError, KeyError, ValueError):
                            # Skip malformed lines - they might be incomplete writes
                            continue

            if records:
                request = logger_pb2.StoreRecordBatchRequest(
                    run_id=header_data.get("run_id"),
                    project=header_data.get("project"),
                    type=file_obj.file_type.value,
                    records=records,
                )

                await make_request(self.client, "StoreRecordBatch", request)

        except Exception:
            # Restore file on error
            if temp_file.exists():
                temp_file.rename(file_obj.path)
            raise
        finally:
            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()

    def _send_file_data_sync(self, file_obj: File, record_type: str) -> None:
        """Send file data to the server synchronously."""
        # Use asyncio.run to call the async version
        asyncio.run(self._send_file_data_async(file_obj))

    def upload_worker(self) -> None:
        """Background worker to upload data files."""
        while not self._stop_upload.is_set():
            try:
                for file_type in FILE_MAP.keys():
                    file_obj = self.file_manager.get_file(file_type.name)
                    should_upload = False
                    with file_obj.lock:
                        if file_obj.exists() and self._should_upload_file(file_obj):
                            should_upload = True

                    if should_upload:
                        self._send_file_data_sync(file_obj, file_type.name)

                time.sleep(1)  # Check every second
            except Exception:
                time.sleep(5)  # Wait longer on error
