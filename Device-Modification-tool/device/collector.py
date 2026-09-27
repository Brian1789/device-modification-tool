from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re

from adb import AdbError, AdbManager


@dataclass
class DeviceInfo:
    serial: str
    state: str
    manufacturer: str = "unknown"
    model: str = "unknown"
    android_version: str = "unknown"
    sdk_version: str = "unknown"
    build_id: str = "unknown"
    architecture: str = "unknown"
    abi: str = "unknown"
    kernel: str = "unknown"
    screen_resolution: str = "unknown"
    ram: str = "unknown"
    storage: str = "unknown"
    security_patch: str = "unknown"
    bootloader_state: str = "unknown"
    root_available: bool = False
    magisk_installed: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


class DeviceInfoCollector:
    def __init__(self, adb: AdbManager):
        self.adb = adb

    def collect(self, serial: str | None = None) -> DeviceInfo:
        devices = self.adb.list_devices()
        selected = next((item for item in devices if serial is None or item.serial == serial), None)
        if selected is None:
            raise AdbError("No matching device is connected.")
        info = DeviceInfo(serial=selected.serial, state=selected.state)
        if selected.state != "device":
            return info
        props = self.adb.get_properties(selected.serial)
        info.manufacturer = props.get("ro.product.manufacturer", "unknown")
        info.model = props.get("ro.product.model", "unknown")
        info.android_version = props.get("ro.build.version.release", "unknown")
        info.sdk_version = props.get("ro.build.version.sdk", "unknown")
        info.build_id = props.get("ro.build.id", "unknown")
        info.architecture = props.get("ro.product.cpu.abilist", props.get("ro.product.cpu.abi", "unknown"))
        info.abi = props.get("ro.product.cpu.abi", "unknown")
        info.security_patch = props.get("ro.build.version.security_patch", "unknown")
        info.kernel = self._shell_value(selected.serial, "uname -a")
        info.screen_resolution = self._shell_value(selected.serial, "wm size")
        info.ram = self._shell_value(selected.serial, "cat /proc/meminfo | head -n 3")
        info.storage = self._shell_value(selected.serial, "df -h /data")
        info.bootloader_state = self._bootloader_state(selected.serial)
        info.root_available = self._root_available(selected.serial)
        info.magisk_installed = self._magisk_installed(selected.serial)
        return info

    def _shell_value(self, serial: str, command: str) -> str:
        try:
            return self.adb.shell(command, serial).stdout
        except AdbError:
            return "unavailable"

    def _bootloader_state(self, serial: str) -> str:
        value = self._shell_value(serial, "getprop ro.boot.verifiedbootstate")
        return value or "unknown"

    def _root_available(self, serial: str) -> bool:
        try:
            return self.adb.shell("id", serial).stdout.startswith("uid=0")
        except AdbError:
            return False

    def _magisk_installed(self, serial: str) -> bool:
        try:
            result = self.adb.shell("command -v magisk", serial)
            return bool(result.stdout.strip())
        except AdbError:
            return False

    @staticmethod
    def format_text(info: DeviceInfo) -> str:
        labels = {key.replace("_", " ").title(): value for key, value in info.to_dict().items()}
        return "\n".join(f"{key}: {json.dumps(value) if isinstance(value, bool) else value}" for key, value in labels.items())
