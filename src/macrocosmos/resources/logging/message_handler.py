import json
import os
import sys
import threading
from datetime import datetime
from typing import Optional

# Import File type for type annotation
from macrocosmos.resources.logging.file_manager import File
from macrocosmos.resources.logging.run import Run

# Conditional import for Windows-specific types and functions
if sys.platform == "win32":
    import ctypes
    import msvcrt
    from ctypes import wintypes

    # Define necessary Windows API types and constants
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12

    # Ctypes function prototypes
    CreatePipe = ctypes.windll.kernel32.CreatePipe
    CreatePipe.argtypes = [
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.POINTER(wintypes.HANDLE),
        ctypes.c_void_p,
        wintypes.DWORD,
    ]
    CreatePipe.restype = wintypes.BOOL

    SetStdHandle = ctypes.windll.kernel32.SetStdHandle
    SetStdHandle.argtypes = [wintypes.DWORD, wintypes.HANDLE]
    SetStdHandle.restype = wintypes.BOOL

    GetStdHandle = ctypes.windll.kernel32.GetStdHandle
    GetStdHandle.argtypes = [wintypes.DWORD]
    GetStdHandle.restype = wintypes.HANDLE

    CloseHandle = ctypes.windll.kernel32.CloseHandle
    CloseHandle.argtypes = [wintypes.HANDLE]
    CloseHandle.restype = wintypes.BOOL

    DuplicateHandle = ctypes.windll.kernel32.DuplicateHandle
    GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess


class ConsoleCapture:
    """
    Captures all stdout and stderr output to a file using low-level,
    OS-specific handle/file-descriptor redirection. Buffers data line-by-line.
    """

    def __init__(self, log_file: File, run: Run):
        self.log_file = log_file
        self.run = run
        self.is_windows = sys.platform == "win32"
        self._capturing = False

        self._stdout_reader_thread: Optional[threading.Thread] = None
        self._stderr_reader_thread: Optional[threading.Thread] = None

        # Platform-specific state
        if self.is_windows:
            self._orig_stdout_handle: Optional[wintypes.HANDLE] = None
            self._orig_stderr_handle: Optional[wintypes.HANDLE] = None
            self._stdout_pipe_write: Optional[wintypes.HANDLE] = None
            self._stderr_pipe_write: Optional[wintypes.HANDLE] = None
            # Keep track of CRT fds for pipe write ends so we can close them cleanly
            self._stdout_write_fd: Optional[int] = None
            self._stderr_write_fd: Optional[int] = None
            self._orig_stdout_fd: Optional[int] = None
            self._orig_stderr_fd: Optional[int] = None
        else:
            self._orig_stdout_fd: Optional[int] = None
            self._orig_stderr_fd: Optional[int] = None
            self._stdout_pipe_write: Optional[int] = None
            self._stderr_pipe_write: Optional[int] = None

    def _log_data(self, data: str, stream_name: str):
        """Helper to write captured data to the log file."""
        if not data:
            return
        timestamp = datetime.now().isoformat()
        record = {
            "timestamp": timestamp,
            "payload_json": json.dumps({"stream": stream_name, "data": data}),
            "payload_name": f"{stream_name}_output",
        }

        # Use the File object's write method which handles locking
        try:
            self.log_file.write(json.dumps(record) + "\n")
        except Exception:
            # Best-effort logging; ignore I/O errors to keep program running
            pass

    def start_capture(self):
        """Start capturing stdout and stderr."""
        if self._capturing:
            return
        self._capturing = True

        # Check if file exists and has header, write header if needed
        with self.log_file.lock:
            if not self.log_file.exists():
                # Use the File object's write_run_header_from_run method which handles locking
                self.log_file.write_run_header_from_run(self.run, auto_lock=False)

        if self.is_windows:
            self._start_windows_capture()
        else:
            self._start_posix_capture()

    def stop_capture(self):
        """Stop capturing and restore original streams."""
        if not self._capturing:
            return
        self._capturing = False  # Signal threads to stop
        if self.is_windows:
            self._stop_windows_capture()
        else:
            self._stop_posix_capture()

    def _line_reader(self, read_fd: int, forward_fd: int, stream_name: str):
        """
        Reads from a file descriptor line-by-line, logs the data, and
        forwards it to another file descriptor. Used by both POSIX and Windows.
        """
        try:
            with os.fdopen(
                read_fd, "r", encoding="utf-8", errors="replace", buffering=1
            ) as reader:
                for line in reader:
                    self._log_data(line.rstrip(), stream_name)
                    try:
                        os.write(forward_fd, line.encode("utf-8", "replace"))
                    except OSError:
                        # Forwarding might fail if the original descriptor is closed
                        pass
        finally:
            # Clean up the forwarding descriptor
            try:
                os.close(forward_fd)
            except OSError:
                pass

    # -----------------------------------------------------
    # POSIX Implementation
    # -----------------------------------------------------
    def _start_posix_capture(self):
        # Save originals
        self._orig_stdout_fd = os.dup(1)
        self._orig_stderr_fd = os.dup(2)

        # Create pipes
        stdout_pipe_read, self._stdout_pipe_write = os.pipe()
        stderr_pipe_read, self._stderr_pipe_write = os.pipe()

        # Redirect
        os.dup2(self._stdout_pipe_write, 1)
        os.dup2(self._stderr_pipe_write, 2)

        # Start reader threads
        self._stdout_reader_thread = threading.Thread(
            target=self._line_reader,
            args=(stdout_pipe_read, self._orig_stdout_fd, "stdout"),
            daemon=True,
        )
        self._stderr_reader_thread = threading.Thread(
            target=self._line_reader,
            args=(stderr_pipe_read, self._orig_stderr_fd, "stderr"),
            daemon=True,
        )
        self._stdout_reader_thread.start()
        self._stderr_reader_thread.start()

    def _stop_posix_capture(self):
        # Restore original descriptors first to prevent subprocesses from hanging
        if self._orig_stdout_fd is not None:
            try:
                os.dup2(self._orig_stdout_fd, 1)
            except OSError:
                pass
        if self._orig_stderr_fd is not None:
            try:
                os.dup2(self._orig_stderr_fd, 2)
            except OSError:
                pass

        # Closing write ends signals readers to exit
        if self._stdout_pipe_write is not None:
            try:
                os.close(self._stdout_pipe_write)
            except OSError:
                pass
        if self._stderr_pipe_write is not None:
            try:
                os.close(self._stderr_pipe_write)
            except OSError:
                pass

        # Join threads
        if self._stdout_reader_thread:
            self._stdout_reader_thread.join(timeout=1)
        if self._stderr_reader_thread:
            self._stderr_reader_thread.join(timeout=1)

    # -----------------------------------------------------
    # Windows Implementation
    # -----------------------------------------------------
    def _start_windows_capture(self):
        # Save original handles
        self._orig_stdout_handle = GetStdHandle(STD_OUTPUT_HANDLE)
        self._orig_stderr_handle = GetStdHandle(STD_ERROR_HANDLE)

        # Duplicate originals so we can create CRT file descriptors without
        # risking closing the real console handles when the fds are closed.
        dup_stdout = wintypes.HANDLE()
        dup_stderr = wintypes.HANDLE()
        DuplicateHandle(
            GetCurrentProcess(),
            self._orig_stdout_handle,
            GetCurrentProcess(),
            ctypes.byref(dup_stdout),
            0,
            False,
            2,  # DUPLICATE_SAME_ACCESS
        )
        DuplicateHandle(
            GetCurrentProcess(),
            self._orig_stderr_handle,
            GetCurrentProcess(),
            ctypes.byref(dup_stderr),
            0,
            False,
            2,
        )

        # Create C-runtime file descriptors for original handles (for restore and forwarding)
        self._orig_stdout_fd = msvcrt.open_osfhandle(dup_stdout.value, 0)
        self._orig_stderr_fd = msvcrt.open_osfhandle(dup_stderr.value, 0)

        # Create pipes
        stdout_pipe_read_h = wintypes.HANDLE()
        self._stdout_pipe_write = wintypes.HANDLE()
        CreatePipe(
            ctypes.byref(stdout_pipe_read_h),
            ctypes.byref(self._stdout_pipe_write),
            None,
            0,
        )

        stderr_pipe_read_h = wintypes.HANDLE()
        self._stderr_pipe_write = wintypes.HANDLE()
        CreatePipe(
            ctypes.byref(stderr_pipe_read_h),
            ctypes.byref(self._stderr_pipe_write),
            None,
            0,
        )

        # Convert pipe handles to C file descriptors
        stdout_read_fd = msvcrt.open_osfhandle(stdout_pipe_read_h.value, os.O_RDONLY)
        stderr_read_fd = msvcrt.open_osfhandle(stderr_pipe_read_h.value, os.O_RDONLY)

        # Create CRT fds for pipe write handles and redirect FD 1/2 so Python prints are captured
        self._stdout_write_fd = msvcrt.open_osfhandle(self._stdout_pipe_write.value, 0)
        self._stderr_write_fd = msvcrt.open_osfhandle(self._stderr_pipe_write.value, 0)

        # Redirect CRT file descriptors so Python-level writes are intercepted
        os.dup2(self._stdout_write_fd, 1)
        os.dup2(self._stderr_write_fd, 2)

        # Forwarding fds are duplicates of the originals (safe to pass to thread)
        stdout_forward_fd = self._orig_stdout_fd
        stderr_forward_fd = self._orig_stderr_fd

        # Start reader threads using the unified line reader
        self._stdout_reader_thread = threading.Thread(
            target=self._line_reader,
            args=(stdout_read_fd, stdout_forward_fd, "stdout"),
            daemon=True,
        )
        self._stderr_reader_thread = threading.Thread(
            target=self._line_reader,
            args=(stderr_read_fd, stderr_forward_fd, "stderr"),
            daemon=True,
        )
        self._stdout_reader_thread.start()
        self._stderr_reader_thread.start()

    def _stop_windows_capture(self):
        # Restore original handles
        if self._orig_stdout_handle is not None:
            try:
                SetStdHandle(STD_OUTPUT_HANDLE, self._orig_stdout_handle)
            except OSError:
                pass
        if self._orig_stderr_handle is not None:
            try:
                SetStdHandle(STD_ERROR_HANDLE, self._orig_stderr_handle)
            except OSError:
                pass

        # Restore CRT file descriptors so further prints work after capture stops
        try:
            if self._orig_stdout_fd is not None:
                os.dup2(self._orig_stdout_fd, 1)
            if self._orig_stderr_fd is not None:
                os.dup2(self._orig_stderr_fd, 2)
        except OSError:
            pass

        # Close pipe write file descriptors to notify readers they should exit
        for fd in (self._stdout_write_fd, self._stderr_write_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass

        # Closing win32 handles (they will be closed when fd closed). best-effort
        if self._stdout_reader_thread:
            self._stdout_reader_thread.join(timeout=1)
        if self._stderr_reader_thread:
            self._stderr_reader_thread.join(timeout=1)

        # Reset Windows-specific placeholders
        self._stdout_write_fd = None
        self._stderr_write_fd = None
