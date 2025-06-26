import threading
import time
import concurrent.futures
from typing import List

from macrocosmos.resources.logging.file_manager import (
    File,
    FileManager,
    FILE_MAP,
    TEMP_FILE_SUFFIX,
)
from macrocosmos.resources.logging.upload_worker import UploadWorker

MAX_BATCH_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
MIN_FILE_AGE_SEC = 10  # 10 seconds


class FileMonitor:
    """Background monitor for checking if files are ready to be uploaded."""

    def __init__(
        self,
        file_manager: FileManager,
        stop_monitoring: threading.Event,
        upload_worker: UploadWorker,
        thread_pool: concurrent.futures.ThreadPoolExecutor,
        upload_futures: List[concurrent.futures.Future],
    ):
        """
        Initialize the file monitor.

        Args:
            file_manager: The file manager instance.
            stop_monitoring: The stop event for the monitoring thread.
            upload_worker: The upload worker to use when a file is ready for upload.
            thread_pool: The thread pool for upload operations.
            upload_futures: The list of upload futures to wait for.
        """
        self.file_manager = file_manager
        self._stop_monitoring = stop_monitoring
        self._upload_worker = upload_worker
        self._thread_pool = thread_pool
        self._upload_futures = upload_futures

    def _should_upload_file(self, file_obj: File) -> bool:
        """Check if a file should be uploaded based on size and time."""
        # Note: This method is called while holding the file lock, so file existence
        # should be stable, but we still handle potential race conditions defensively
        try:
            if not file_obj.exists():
                return False

            tmp_file_path = file_obj.path.with_suffix(
                file_obj.path.suffix + TEMP_FILE_SUFFIX
            )
            if tmp_file_path.exists():
                # There is an upload in progress, we will keep appending to the current file
                return False

            # Get file stats once to avoid multiple stat calls
            stat_info = file_obj.path.stat()

            # Check file size (>5MB)
            if stat_info.st_size > MAX_BATCH_SIZE_BYTES:
                return True

            # Check if there are records to upload (excluding header)
            if (
                file_obj.age
                and file_obj.age > MIN_FILE_AGE_SEC
                and file_obj.has_records()
            ):
                return True

            return False
        except (OSError, IOError):
            # File was deleted or became inaccessible between checks
            return False

    def monitor_files(self) -> None:
        """Background worker to monitor files for upload readiness."""
        while not self._stop_monitoring.is_set():
            try:
                for file_type in FILE_MAP.keys():
                    file_obj = self.file_manager.get_file(file_type)
                    file_obj.lock.acquire()  # NOTE: This lock will be released by the `upload_file` method or the below else clause
                    if file_obj.exists() and self._should_upload_file(file_obj):
                        # Submit upload task to thread pool if available
                        future = self._thread_pool.submit(
                            self._upload_worker.upload_file,
                            file_obj,
                            early_lock_release=True,
                        )
                        self._upload_futures.append(future)
                    else:
                        file_obj.lock.release()
                time.sleep(1)  # Check every second
            except Exception:
                time.sleep(5)  # Wait longer on error
