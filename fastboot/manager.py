from __future__ import annotations

import shutil
import subprocess


class FastbootManager:
    def __init__(self, executable: str = "fastboot", timeout: float = 15.0):
        self.executable = executable
        self.timeout = timeout

    def is_installed(self) -> bool:
        return shutil.which(self.executable) is not None

    def devices(self) -> list[str]:
        result = subprocess.run([self.executable, "devices"], capture_output=True, text=True, timeout=self.timeout, check=False)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "Fastboot failed")
        return [line.split()[0] for line in result.stdout.splitlines() if line.split()]
