from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


class Run:
    """Represents a logging run with all its metadata."""

    def __init__(
        self,
        run_id: str,
        project: str,
        entity: str,
        name: str,
        description: Optional[str] = None,
        notes: Optional[str] = None,
        tags: Optional[List[str]] = None,
        config: Optional[Dict[str, Any]] = None,
        start_time: Optional[datetime] = None,
        initial_step: Optional[int] = 0,
        finish_callback: Optional[Callable[[], None]] = None,
    ):
        """
        Initialize a new run.

        Args:
            run_id: Unique identifier for the run
            project: Project name
            entity: Entity name
            name: Run name
            description: Optional description
            notes: Optional notes
            tags: Optional list of tags
            config: Optional configuration dictionary
            start_time: Optional start time (defaults to current time)
            initial_step: Optional initial step number (defaults to 0)
            finish_callback: Optional callback to call when the run is finished
        """
        self.run_id = run_id
        self.project = project
        self.entity = entity
        self.name = name
        self.description = description
        self.notes = notes
        self.tags = tags or []
        self.config = config or {}
        self.start_time = start_time or datetime.now()
        self.step = initial_step or 0
        self._finish_callback = finish_callback
        self._finish_time: Optional[datetime] = None

    def to_header_dict(self) -> Dict[str, Any]:
        """Convert run metadata to a header dictionary for file writing."""
        return {
            "__type": "header",
            "run_id": self.run_id,
            "project": self.project,
            "entity": self.entity,
            "name": self.name,
            "description": self.description,
            "notes": self.notes,
            "tags": self.tags,
            "config": self.config,
            "created_at": self.start_time.isoformat(),
        }

    def finish(self) -> None:
        """Finish the run and call the finish callback."""
        if self._finish_callback:
            self._finish_callback()
        self._finish_time = datetime.now()

    @property
    def id(self) -> str:
        """Get the run ID."""
        return self.run_id

    @property
    def runtime(self) -> float:
        """Get the current runtime in seconds."""
        return ((self._finish_time or datetime.now()) - self.start_time).total_seconds()

    def next_step(self) -> int:
        """Increment the step number."""
        self.step += 1
        return self.step
