from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from device import DeviceInfoCollector


class BackupManager:
    def __init__(self, collector: DeviceInfoCollector, root: str | Path = "backups"):
        self.collector = collector
        self.root = Path(root)

    def create(self, serial: str | None = None) -> Path:
        info = self.collector.collect(serial)
        self.root.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path = self.root / f"device-state-{info.serial}-{stamp}.json"
        payload = {"created_at": datetime.now(timezone.utc).isoformat(), "device": info.to_dict()}
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return path

    def restore(self, backup_path: str | Path) -> dict:
        path = Path(backup_path)
        if not path.exists():
            raise FileNotFoundError(path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload.get("device"), dict) or "serial" not in payload["device"]:
            raise ValueError("Invalid device backup metadata.")
        return payload

    def verify(self, backup_path: str | Path, serial: str | None = None) -> bool:
        expected = self.restore(backup_path)["device"]
        actual = self.collector.collect(serial).to_dict()
        return expected.get("serial") == actual.get("serial")
