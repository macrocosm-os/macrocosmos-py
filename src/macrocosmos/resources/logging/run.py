from datetime import datetime
from typing import Any, Dict, List, Optional


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

    def to_header_dict(self) -> Dict[str, Any]:
        """Convert run metadata to a header dictionary for file writing."""
        return {
            "type": "header",
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

    @property
    def runtime(self) -> float:
        """Get the current runtime in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
