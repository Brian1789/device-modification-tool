from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from adb import AdbError, AdbManager
from backup import BackupManager
from configuration import ConfigError, ConfigurationManager
from device import DeviceInfoCollector
from diagnostics import DiagnosticsCollector
from logging_tool import StructuredLogger
from magisk import MagiskError, MagiskManager


class Application:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.adb = AdbManager(executable=args.adb)
        self.collector = DeviceInfoCollector(self.adb)
        self.logger = StructuredLogger(Path(args.log_dir) / "application.log")

    def devices(self) -> int:
        if not self.adb.is_installed():
            print("ADB is not installed or is not on PATH.", file=sys.stderr)
            return 1
        for device in self.adb.list_devices():
            print(f"{device.serial}\t{device.state}\t{device.detail}".rstrip())
        return 0

    def info(self) -> int:
        info = self.collector.collect(self.args.serial)
        print(json.dumps(info.to_dict(), indent=2) if self.args.json else DeviceInfoCollector.format_text(info))
        return 0

    def status(self) -> int:
        print(f"ADB installed: {self.adb.is_installed()}")
        try:
            devices = self.adb.list_devices()
        except AdbError as exc:
            print(f"ADB error: {exc}", file=sys.stderr)
            return 1
        print(f"Connected devices: {len(devices)}")
        for device in devices:
            print(f"- {device.serial}: {device.state}")
        return 0

    def shell(self) -> int:
        result = self.adb.shell(self.args.command, self.args.serial)
        if result.stdout:
            print(result.stdout)
        return 0

    def reboot(self) -> int:
        self.adb.reboot(self.args.mode, self.args.serial)
        print("Reboot requested.")
        return 0

    def magisk_status(self) -> int:
        status = MagiskManager(self.adb).status(self.args.serial or self._serial())
        print(json.dumps(status, indent=2))
        return 0

    def magisk_install(self) -> int:
        serial = self.args.serial or self._serial()
        MagiskManager(self.adb).install(serial, self.args.zip_path)
        print("Module installation command completed. Reboot and verify module activation.")
        return 0

    def magisk_remove(self) -> int:
        serial = self.args.serial or self._serial()
        MagiskManager(self.adb).remove(serial, self.args.module_id)
        print("Module removed. Reboot and verify the device.")
        return 0

    def backup(self) -> int:
        path = BackupManager(self.collector, self.args.backup_dir).create(self.args.serial)
        print(path)
        return 0

    def restore(self) -> int:
        payload = BackupManager(self.collector, self.args.backup_dir).restore(self.args.backup_path)
        print(f"Validated backup for device {payload['device']['serial']}; no destructive restore is performed automatically.")
        return 0

    def verify(self) -> int:
        ok = BackupManager(self.collector, self.args.backup_dir).verify(self.args.backup_path, self.args.serial)
        print("verified" if ok else "mismatch")
        return 0 if ok else 1

    def diagnostics(self) -> int:
        report = DiagnosticsCollector(self.adb, self.collector).collect(self.args.serial, self.args.output)
        if not self.args.output:
            print(json.dumps(report, indent=2))
        else:
            print(self.args.output)
        return 0

    def config_backup(self) -> int:
        print(ConfigurationManager(self.args.config_dir).backup())
        return 0

    def _serial(self) -> str:
        devices = [item for item in self.adb.list_devices() if item.state == "device"]
        if len(devices) != 1:
            raise AdbError("Specify --serial when zero or multiple usable devices are connected.")
        return devices[0].serial


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="device-tool", description="Lightweight Android device management toolkit")
    parser.add_argument("--adb", default="adb", help="ADB executable or full path")
    parser.add_argument("--serial", help="Target device serial")
    parser.add_argument("--log-dir", default="logs")
    parser.add_argument("--backup-dir", default="backups")
    parser.add_argument("--config-dir", default="config")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("devices")
    sub.add_parser("status")
    info = sub.add_parser("info"); info.add_argument("--json", action="store_true")
    shell = sub.add_parser("shell"); shell.add_argument("command")
    magisk_parser = sub.add_parser("magisk")
    magisk_sub = magisk_parser.add_subparsers(dest="action", required=True)
    magisk_sub.add_parser("status")
    install = magisk_sub.add_parser("install"); install.add_argument("zip_path")
    remove = magisk_sub.add_parser("remove"); remove.add_argument("module_id")
    backup = sub.add_parser("backup")
    restore = sub.add_parser("restore"); restore.add_argument("backup_path")
    verify = sub.add_parser("verify"); verify.add_argument("backup_path")
    diagnostics = sub.add_parser("diagnostics"); diagnostics.add_argument("--output")
    sub.add_parser("config-backup")
    reboot = sub.add_parser("reboot"); reboot.add_argument("mode", nargs="?")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    app = None
    try:
        app = Application(args)
        if args.command == "devices": result = app.devices()
        elif args.command == "status": result = app.status()
        elif args.command == "info": result = app.info()
        elif args.command == "shell": result = app.shell()
        elif args.command == "reboot": result = app.reboot()
        elif args.command == "magisk" and args.action == "status": result = app.magisk_status()
        elif args.command == "magisk" and args.action == "install": result = app.magisk_install()
        elif args.command == "magisk" and args.action == "remove": result = app.magisk_remove()
        elif args.command == "backup": result = app.backup()
        elif args.command == "restore": result = app.restore()
        elif args.command == "verify": result = app.verify()
        elif args.command == "diagnostics": result = app.diagnostics()
        elif args.command == "config-backup": result = app.config_backup()
        else: parser.error("Unknown command")
        app.logger.event(args.command, "ok" if result == 0 else "failed", device=args.serial)
        return result
    except (AdbError, ConfigError, MagiskError, FileNotFoundError, ValueError) as exc:
        if app is not None:
            app.logger.event(args.command, "error", device=args.serial, error=str(exc))
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
