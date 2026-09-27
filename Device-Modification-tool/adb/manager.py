from __future__ import annotations

from dataclasses import dataclass
import os
import shutil
import subprocess
from typing import Sequence


class AdbError(RuntimeError):
    """An ADB executable or device operation failed."""


@dataclass(frozen=True)
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class DeviceRecord:
    serial: str
    state: str
    detail: str = ""


class AdbManager:
    def __init__(self, executable: str = "adb", timeout: float = 15.0, runner=None):
        self.executable = executable
        self.timeout = timeout
        self._runner = runner or subprocess.run

    def is_installed(self) -> bool:
        return shutil.which(self.executable) is not None

    def _run(self, args: Sequence[str], timeout: float | None = None) -> CommandResult:
        command = [self.executable, *args]
        try:
            completed = self._runner(
                command,
                capture_output=True,
                text=True,
                timeout=timeout or self.timeout,
                check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except FileNotFoundError as exc:
            raise AdbError("ADB was not found. Install Android platform-tools and add adb to PATH.") from exc
        except subprocess.TimeoutExpired as exc:
            raise AdbError(f"ADB command timed out after {timeout or self.timeout:.1f}s: {' '.join(command)}") from exc
        return CommandResult(command, completed.returncode, completed.stdout.strip(), completed.stderr.strip())

    def _require_ok(self, result: CommandResult) -> CommandResult:
        if not result.ok:
            message = result.stderr or result.stdout or "unknown ADB error"
            raise AdbError(message)
        return result

    def list_devices(self) -> list[DeviceRecord]:
        result = self._require_ok(self._run(["devices", "-l"]))
        devices: list[DeviceRecord] = []
        for line in result.stdout.splitlines()[1:]:
            fields = line.split()
            if len(fields) >= 2 and fields[0] != "*":
                detail = " ".join(fields[2:])
                devices.append(DeviceRecord(fields[0], fields[1], detail))
        return devices

    def shell(self, command: str, serial: str | None = None, timeout: float | None = None) -> CommandResult:
        args = (["-s", serial] if serial else []) + ["shell", command]
        result = self._run(args, timeout)
        if result.returncode != 0:
            state = "unauthorized or offline device" if "unauthorized" in result.stderr.lower() or "offline" in result.stderr.lower() else "shell command failed"
            raise AdbError(f"{state}: {result.stderr or result.stdout}")
        return result

    def get_properties(self, serial: str | None = None) -> dict[str, str]:
        output = self.shell("getprop", serial).stdout
        properties: dict[str, str] = {}
        for line in output.splitlines():
            if line.startswith("[") and "]: [" in line and line.endswith("]"):
                key, value = line[1:].split("]: [", 1)
                properties[key] = value[:-1]
        return properties

    def reboot(self, mode: str | None = None, serial: str | None = None) -> CommandResult:
        args = (["-s", serial] if serial else []) + ["reboot"] + ([mode] if mode else [])
        return self._require_ok(self._run(args))

    def push(self, local: str, remote: str, serial: str | None = None) -> CommandResult:
        if not os.path.isfile(local):
            raise AdbError(f"Local file does not exist: {local}")
        args = (["-s", serial] if serial else []) + ["push", local, remote]
        return self._require_ok(self._run(args))

    def pull(self, remote: str, local: str, serial: str | None = None) -> CommandResult:
        args = (["-s", serial] if serial else []) + ["pull", remote, local]
        return self._require_ok(self._run(args))
