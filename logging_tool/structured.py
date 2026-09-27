from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


class StructuredLogger:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def event(self, operation: str, result: str, device: str | None = None, error: str | None = None, **fields: Any) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": operation,
            "device": device,
            "result": result,
            "error": error,
            **fields,
        }
        self.path.open("a", encoding="utf-8").write(json.dumps(record, sort_keys=True) + "\n")
