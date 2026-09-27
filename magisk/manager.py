from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from adb import AdbError, AdbManager


class MagiskError(RuntimeError):
    pass


@dataclass(frozen=True)
class ModuleRecord:
    module_id: str
    name: str
    version: str
    enabled: bool


class MagiskManager:
    def __init__(self, adb: AdbManager, state_file: str | Path = "config/magisk-state.json"):
        self.adb = adb
        self.state_file = Path(state_file)

    def status(self, serial: str) -> dict[str, bool]:
        try:
            self.adb.shell("command -v magisk", serial)
            installed = True
        except AdbError:
            installed = False
        try:
            rooted = self.adb.shell("id", serial).stdout.startswith("uid=0")
        except AdbError:
            rooted = False
        return {"installed": installed, "root_available": rooted}

    def list_modules(self, serial: str) -> list[ModuleRecord]:
        try:
            output = self.adb.shell("ls -1 /data/adb/modules", serial).stdout
        except AdbError as exc:
            raise MagiskError("Magisk modules are unavailable; verify root and Magisk installation.") from exc
        modules: list[ModuleRecord] = []
        for module_id in output.splitlines():
            module_id = module_id.strip()
            if not module_id or module_id.startswith("."):
                continue
            name = self._read_module_prop(serial, module_id, "name") or module_id
            version = self._read_module_prop(serial, module_id, "version") or "unknown"
            enabled = not self._module_marker_exists(serial, module_id, "disable")
            modules.append(ModuleRecord(module_id, name, version, enabled))
        return modules

    def _read_module_prop(self, serial: str, module_id: str, key: str) -> str:
        try:
            output = self.adb.shell(f"su -c 'grep ^{key}= /data/adb/modules/{module_id}/module.prop'", serial).stdout
            return output.split("=", 1)[1].strip() if "=" in output else ""
        except AdbError:
            return ""

    def _module_marker_exists(self, serial: str, module_id: str, marker: str) -> bool:
        try:
            return self.adb.shell(f"su -c 'test -e /data/adb/modules/{module_id}/{marker}'", serial).ok
        except AdbError:
            return False

    def install(self, serial: str, zip_path: str | Path) -> None:
        path = Path(zip_path)
        if path.suffix.lower() != ".zip" or not path.is_file():
            raise MagiskError("Module must be an existing local .zip file.")
        remote = "/data/local/tmp/device-tool-module.zip"
        self.adb.push(str(path), remote, serial)
        try:
            self.adb.shell(f"su -c 'magisk --install-module {remote}'", serial, timeout=60)
        except AdbError as exc:
            raise MagiskError("Magisk module installation failed; inspect device logs.") from exc
        finally:
            try:
                self.adb.shell(f"rm -f {remote}", serial)
            except AdbError:
                pass

    def remove(self, serial: str, module_id: str) -> None:
        if not module_id or "/" in module_id or " " in module_id:
            raise MagiskError("Invalid module id.")
        self.adb.shell(f"su -c 'rm -rf /data/adb/modules/{module_id}'", serial)

    def set_enabled(self, serial: str, module_id: str, enabled: bool) -> None:
        if not module_id or "/" in module_id or " " in module_id:
            raise MagiskError("Invalid module id.")
        marker = "disable"
        command = f"su -c 'rm -f /data/adb/modules/{module_id}/{marker}'" if enabled else f"su -c 'touch /data/adb/modules/{module_id}/{marker}'"
        self.adb.shell(command, serial)
