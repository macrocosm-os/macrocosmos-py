import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

from google.protobuf import timestamp_pb2
from macrocosmos.generated.logger.v1 import logger_pb2
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources.logging.file_manager import (
    File,
    FileType,
    TEMP_FILE_SUFFIX,
)
from macrocosmos.resources.logging.request import make_sync_request

MAX_BATCH_SIZE_BYTES = 5 * 1024 * 1024  # 5MB


class UploadWorker:
    """Worker for uploading files in bathces to the server."""

    def __init__(
        self,
        client: BaseClient,
        stop_upload: threading.Event,
    ):
        """
        Initialize the upload worker.

        Args:
            client: The client instance for making requests.
            stop_upload: The stop event for the upload thread.
        """
        self.client = client
        self._stop_upload = stop_upload

    def upload_file(
        self,
        file_obj: File,
        temp_file: Optional[Path] = None,
        early_lock_release: bool = False,
    ) -> None:
        """
        Upload a single file to the server using checkpoint-based processing.

        Args:
            file_obj (File): The file object representing the log file to be sent.
                             This file must be locked before calling this method.
            temp_file (Optional[Path]): An optional path to a temporary file. If provided,
                                        this file will be used directly for sending data,
                                        typically for recovery of orphaned temp files.
            early_lock_release (bool): A flag indicating whether to release the file lock
                                       immediately after renaming the file. Use this when the
                                       lock was manually "acquired" instead of a context
                                       manager. Read below for more details. Defaults to False.
        """
        # WARNING: do not put any code above in this area as an unexpected failure will not release the blocking lock for the file monitor
        try:
            if self._stop_upload.is_set():
                return

            # Read header to get run info
            header_data = file_obj.read_file_header()
            if not header_data:
                raise ValueError(
                    "run_id and project are required for sending file data"
                )

            # If temp_file is provided, use it directly (for recovery of orphaned temp files)
            # Otherwise, check if there are records and rename the file
            if temp_file is None:
                temp_file = file_obj.path.with_suffix(
                    file_obj.path.suffix + TEMP_FILE_SUFFIX
                )

                # Check if there are records before renaming
                if not file_obj.has_records():
                    # No records, just clean up the file
                    if file_obj.path.exists():
                        file_obj.path.unlink()
                    return
                file_obj.path.rename(temp_file)
        except Exception:
            raise
        finally:
            # WARNING: do not remove this logic to ensure the lock gets cleared for the file monitor
            if early_lock_release:
                # This is to reduce blocking locks on writes to the file while a run is running
                # It does this by releasing the lock on this file early since the file has been renamed
                # so concurrent writes can happen while the rest of this process runs.
                file_obj.lock.release()

        # Create checkpoint file for tracking progress
        checkpoint_file = temp_file.with_suffix(".checkpoint")

        try:
            # Read checkpoint if exists to resume from previous position
            start_index = 0
            if checkpoint_file.exists():
                try:
                    with open(checkpoint_file, "r") as f:
                        start_index = int(f.read().strip())
                except (ValueError, IOError):
                    # Invalid checkpoint, start from beginning
                    start_index = 0

            # Process file in batches with checkpoint tracking
            self._process_file_with_checkpoints(
                temp_file,
                checkpoint_file,
                header_data,
                file_obj.file_type,
                start_index,
            )

            if not self._stop_upload.is_set():
                # Success - clean up checkpoint and tempfile
                if checkpoint_file.exists():
                    checkpoint_file.unlink()
                if temp_file.exists():
                    temp_file.unlink()

        except Exception:
            # Keep checkpoint file for recovery on next attempt
            raise

    def _process_file_with_checkpoints(
        self,
        temp_file: Path,
        checkpoint_file: Path,
        header_data: dict,
        file_type: FileType,
        start_index: int,
    ) -> None:
        """
        Process file in batches with checkpoint-based recovery.

        Args:
            temp_file: Path to the temporary file to process.
            checkpoint_file: Path to the checkpoint file for tracking progress.
            header_data: Header data containing run_id and project.
            file_type: Type of file being processed.
            start_index: Index to start processing from (0-based).
        """
        with open(temp_file, "r") as f:
            # Skip header
            f.readline()

            # Skip to checkpoint position
            # For example, `start_index = 1` means we skip the first line after the header
            # (we call `readline()` one more time since we called it just above)
            for _ in range(start_index):
                f.readline()

            current_batch = []
            current_batch_size = 0
            line_index = start_index
            batches_sent = 0

            while not self._stop_upload.is_set():
                line = f.readline()
                if not line:
                    break

                # Increment line_index for every line we read (0-based)
                line_index += 1

                if line.strip():
                    try:
                        record_data = json.loads(line)

                        # Skip header row (shouldn't happen in normal operation, but handle defensively)
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

                        record_size = len(record.payload_json.encode("utf-8"))

                        # Check if adding this record would exceed batch limits
                        if current_batch_size + record_size > MAX_BATCH_SIZE_BYTES:
                            # Send current batch
                            if current_batch:
                                self._send_batch(current_batch, header_data, file_type)
                                batches_sent += 1

                                # Update checkpoint after successful batch send
                                self._update_checkpoint(checkpoint_file, line_index)

                                current_batch = []
                                current_batch_size = 0

                        current_batch.append(record)
                        current_batch_size += record_size

                    except (json.JSONDecodeError, KeyError, ValueError):
                        # Skip malformed lines - they might be incomplete writes
                        continue

            # Send final batch - or when the upload is stopped
            if current_batch:
                self._send_batch(current_batch, header_data, file_type)
                batches_sent += 1
                self._update_checkpoint(checkpoint_file, line_index)

    def _send_batch(
        self, records: list, header_data: dict, file_type: FileType
    ) -> None:
        """
        Send a single batch of records to the server.

        Args:
            records: List of Record objects to send.
            header_data: Header data containing run_id and project.
            file_type: Type of file being processed.
        """
        request = logger_pb2.StoreRecordBatchRequest(
            run_id=header_data.get("run_id"),
            project=header_data.get("project"),
            type=file_type.value,
            records=records,
        )

        make_sync_request(self.client, "StoreRecordBatch", request)

    def _update_checkpoint(self, checkpoint_file: Path, line_index: int) -> None:
        """
        Update the checkpoint file with current line index.

        Args:
            checkpoint_file: Path to the checkpoint file.
            line_index: Current line index (0-based).
        """
        try:
            with open(checkpoint_file, "w") as f:
                f.write(str(line_index))
        except IOError:
            # If we can't write checkpoint, continue processing
            # The checkpoint will be recreated on next attempt
            pass
