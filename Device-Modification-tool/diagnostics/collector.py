from __future__ import annotations

import json
from pathlib import Path

from adb import AdbManager
from device import DeviceInfoCollector


class DiagnosticsCollector:
    def __init__(self, adb: AdbManager, device_info: DeviceInfoCollector):
        self.adb = adb
        self.device_info = device_info

    def collect(self, serial: str | None = None, output: str | Path | None = None) -> dict:
        info = self.device_info.collect(serial)
        report = {"device": info.to_dict()}
        if output:
            path = Path(output)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return report
