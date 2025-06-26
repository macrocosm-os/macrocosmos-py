import json
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

from macrocosmos.resources.logging.run import Run

from enum import Enum


class FileType(str, Enum):
    LOG = "log"
    HISTORY = "history"


TEMP_FILE_SUFFIX = ".tmp"
FILE_MAP = {
    FileType.LOG: "logs.jsonl",
    FileType.HISTORY: "history.jsonl",
}


class File:
    """Represents a log file with its associated lock."""

    def __init__(self, path: Path, file_type: FileType, run: Optional[Run] = None):
        self.path = path
        self.file_type = file_type
        self.lock = threading.Lock()
        self.run = run
        self.creation_time: Optional[float] = None  # Track actual file creation time

    def write(self, content: str, auto_lock: bool = True) -> None:
        """Write content to the file with lock protection (append mode)."""
        if auto_lock:
            with self.lock:
                self._write(content)
        else:
            # when `auto_lock=False` we are assuming a lock is already inplace
            # if we were to try to lock when the lock is already in place (even if it's the same thread)
            # we'd block ourselves (console_handler._log_data).
            # NOTE: an RLock won't work for self.lock since we have some locks that are released by
            # threads that did not create the lock (monitor_files > upload_file)
            self._write(content)

    def _write(self, content: str, auto_lock: bool = True) -> None:
        """Write content to the file with lock protection (append mode)."""
        # Transparently create the directory if it disappeared between runs
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # If requested, write the header first when the file is missing.
        if self.run is not None and not self.path.exists():
            # Track creation time when we actually create the file
            self.creation_time = time.time()
            header_dict = self.run.to_header_dict()
            header_dict["type"] = self.file_type.value
            header_line = json.dumps(header_dict) + "\n"
            # Ensure we start with a fresh file for the header
            with open(self.path, "w") as f:
                f.write(header_line)

        # Now write the actual payload in the desired mode
        with open(self.path, "a") as f:
            f.write(content)

    @property
    def age(self) -> Optional[float]:
        """Get the age of the file in seconds since it was created."""
        if self.creation_time is None:
            return None
        return time.time() - self.creation_time

    def exists(self) -> bool:
        """Check if the file exists."""
        return self.path.exists()

    def read_file_header(self) -> Optional[Dict[str, Any]]:
        """Read the header row from a file to extract run metadata."""
        # Note: file existence is checked by the caller, so we don't check again here
        # to avoid race conditions

        try:
            with open(self.path, "r") as f:
                first_line = f.readline().strip()
                if first_line:
                    header_data = json.loads(first_line)
                    if header_data.get("__type") == "header":
                        return header_data
        except (json.JSONDecodeError, IOError):
            pass
        return None

    def has_records(self) -> bool:
        """Check if a file has records (excluding header)."""
        # Note: file existence is checked by the caller, so we don't check again here
        # to avoid race conditions

        try:
            with open(self.path, "r") as f:
                # Skip header
                f.readline()
                # Check if second line has content
                second_line = f.readline().strip()
                return bool(second_line)
        except IOError:
            return False


class FileManager:
    """Manages different types of log files with their own locks."""

    def __init__(self, temp_dir: Path, run: Optional[Run] = None):
        self.temp_dir = temp_dir
        self.run = run
        self.history_file = File(
            temp_dir / FILE_MAP[FileType.HISTORY], FileType.HISTORY, run
        )
        self.log_file = File(temp_dir / FILE_MAP[FileType.LOG], FileType.LOG, run)

    def get_file(self, file_type: FileType) -> File:
        """Get the file object for a given file type."""
        if file_type == FileType.HISTORY:
            return self.history_file
        elif file_type == FileType.LOG:
            return self.log_file
        else:
            raise ValueError(f"Unknown file type: {file_type}")
