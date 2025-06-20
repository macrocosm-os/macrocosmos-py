import json
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from macrocosmos.resources.logging.run import Run

from enum import Enum


class FileType(Enum, str):
    LOG = "log"
    HISTORY = "history"


TEMP_FILE_SUFFIX = ".tmp"
LOG_FILE_NAME = "logs.jsonl"
HISTORY_FILE_NAME = "history.jsonl"
FILE_TYPES = {FileType.LOG: LOG_FILE_NAME, FileType.HISTORY: HISTORY_FILE_NAME}

# TODO: we should check our locking behavior and make sure we're attempting to lock something that is already locked
# as well as if a lock might need to be moved because of a race condition we introduced.


class File:
    """Represents a log file with its associated lock."""

    def __init__(self, path: Path, file_type: FileType, run: Optional[Run] = None):
        self.path = path
        self.file_type = file_type
        self.lock = threading.Lock()
        self.run = run

    def write(self, content: str, auto_lock: bool = True) -> None:
        """Write content to the file with lock protection."""
        if auto_lock:
            # Acquire lock ourselves
            with self.lock:
                self._write_with_header_check(content)
        else:
            # Assume lock is already held by caller
            self._write_with_header_check(content)

    def _write_with_header_check(self, content: str) -> None:
        """Write content, recreating file with header if it doesn't exist."""
        if not self.path.exists():
            # File was renamed (sent to server), start a new file with header
            if self.run is not None:
                self.write_run_header_from_run(self.run, auto_lock=False)

        with open(self.path, "a") as f:
            f.write(content)

    def write_header(self, content: str, auto_lock: bool = True) -> None:
        """Write header content to the file with lock protection."""
        if auto_lock:
            # Acquire lock ourselves
            with self.lock:
                with open(self.path, "w") as f:
                    f.write(content)
        else:
            # Assume lock is already held by caller
            with open(self.path, "w") as f:
                f.write(content)

    def write_run_header_from_run(self, run: Run, auto_lock: bool = True) -> None:
        """Write a header row to a file using a Run object."""
        header = run.to_header_dict()
        header["__type"] = "header"
        header["type"] = self.file_type.value
        self.write_header(json.dumps(header) + "\n", auto_lock=auto_lock)

    def exists(self) -> bool:
        """Check if the file exists."""
        return self.path.exists()

    def ends_with_newline(self) -> bool:
        """Check if file ends with a newline character."""
        if not self.exists():
            return False

        try:
            with open(self.path, "rb") as f:
                # Seek to end and check last character
                f.seek(0, 2)  # Seek to end
                if f.tell() == 0:  # Empty file
                    return True
                f.seek(-1, 2)  # Go back 1 byte
                last_char = f.read(1)
                return last_char == b"\n"
        except (OSError, IOError):
            return False

    def read_file_header(self) -> Optional[Dict[str, Any]]:
        """Read the header row from a file to extract run metadata."""
        # Note: file existence is checked by the caller, so we don't check again here
        # to avoid race conditions

        try:
            with open(self.path, "r") as f:
                first_line = f.readline().strip()
                if first_line:
                    header_data = json.loads(first_line)
                    if header_data.get("type") == "header":
                        return header_data
        except (json.JSONDecodeError, IOError):
            pass
        return None


class FileManager:
    """Manages different types of log files with their own locks."""

    def __init__(self, temp_dir: Path, run: Optional[Run] = None):
        self.temp_dir = temp_dir
        self.run = run
        self.history_file = File(temp_dir / HISTORY_FILE_NAME, FileType.HISTORY, run)
        self.log_file = File(temp_dir / LOG_FILE_NAME, FileType.LOG, run)

    def get_file(self, file_type: FileType) -> File:
        """Get the file object for a given file type."""
        if file_type == FileType.HISTORY:
            return self.history_file
        elif file_type == FileType.LOG:
            return self.log_file
        else:
            raise ValueError(f"Unknown file type: {file_type}")
