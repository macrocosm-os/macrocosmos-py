import asyncio
import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from macrocosmos.generated.logger.v1 import logger_pb2
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources.logging.file_manager import (
    File,
    FileManager,
    FILE_MAP,
    TEMP_FILE_SUFFIX,
)
from macrocosmos.resources.logging.request import make_request


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

    def _should_upload_file(self, file_path: Path) -> bool:
        """Check if a file should be uploaded based on size and time."""
        # Note: This method is called while holding the file lock, so file existence
        # should be stable, but we still handle potential race conditions defensively

        try:
            if not file_path.exists():
                return False

            # Get file stats once to avoid multiple stat calls
            stat_info = file_path.stat()

            # Check file size (>5MB)
            if stat_info.st_size > 5 * 1024 * 1024:
                return True

            # Check if there are records to upload (excluding header)
            if self._has_records(file_path):
                # Check file age (>10s) using the stat info we already have
                file_age = time.time() - stat_info.st_mtime
                if file_age > 10:
                    return True

            return False
        except (OSError, IOError):
            # File was deleted or became inaccessible between checks
            return False

    # TODO: this should be a method on the File object
    def _has_records(self, file_path: Path) -> bool:
        """Check if a file has records (excluding header)."""
        # Note: file existence is checked by the caller, so we don't check again here
        # to avoid race conditions

        try:
            with open(file_path, "r") as f:
                # Skip header
                f.readline()
                # Check if second line has content
                second_line = f.readline().strip()
                return bool(second_line)
        except IOError:
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
                if not self._has_records(file_obj.path):
                    # No records, just clean up the file
                    if file_obj.path.exists():
                        file_obj.path.unlink()
                    return
                file_obj.path.rename(temp_file)

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

                            # TODO: need to fix the timestamp type here since the protobuf expects a google.protobuf.Timestamp
                            # TODO: need to consider how the data in the file is formatted to match this expected format
                            record = logger_pb2.Record(
                                timestamp=datetime.fromisoformat(
                                    record_data["timestamp"]
                                ),
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
                # TODO: we need to expand this to include other data needed
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
                        if file_obj.exists() and self._should_upload_file(
                            file_obj.path
                        ):
                            should_upload = True

                    if should_upload:
                        self._send_file_data_sync(file_obj, file_type.name)

                time.sleep(1)  # Check every second
            except Exception:
                time.sleep(5)  # Wait longer on error
