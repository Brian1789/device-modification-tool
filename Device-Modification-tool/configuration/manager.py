from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any


class ConfigError(ValueError):
    pass


class ConfigurationManager:
    def __init__(self, root: str | Path = "config"):
        self.root = Path(root)
        self.default_file = self.root / "default.json"
        self.devices_dir = self.root / "devices"
        self.profiles_dir = self.root / "profiles"
        self.backups_dir = self.root / "backups"

    def load(self) -> dict[str, Any]:
        if not self.default_file.exists():
            return {}
        try:
            with self.default_file.open(encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON in {self.default_file}: {exc}") from exc
        self.validate(data)
        return data

    def load_device(self, serial: str) -> dict[str, Any]:
        path = self.devices_dir / f"{serial}.json"
        if not path.exists():
            return self.load()
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        self.validate(data)
        return data

    @staticmethod
    def validate(data: Any) -> None:
        if not isinstance(data, dict):
            raise ConfigError("Configuration must be a JSON object.")
        for key in ("device", "profile", "settings"):
            if key in data and not isinstance(data[key], (str, dict, list, type(None))):
                raise ConfigError(f"Configuration field '{key}' has an unsupported type.")

    def backup(self, source: str | Path | None = None) -> Path:
        source_path = Path(source) if source else self.default_file
        if not source_path.exists():
            raise ConfigError(f"Cannot back up missing configuration: {source_path}")
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        destination = self.backups_dir / f"{source_path.stem}-{stamp}.json"
        shutil.copy2(source_path, destination)
        return destination

    def restore(self, backup_path: str | Path, destination: str | Path | None = None) -> Path:
        source = Path(backup_path)
        if not source.exists():
            raise ConfigError(f"Backup does not exist: {source}")
        target = Path(destination) if destination else self.default_file
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        self.validate(json.loads(target.read_text(encoding="utf-8")))
        return target
