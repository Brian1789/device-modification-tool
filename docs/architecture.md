# Architecture

The project uses small Python modules and the standard library at runtime.

- `adb/`: subprocess boundary, device listing, shell, properties, push, pull, reboot.
- `fastboot/`: minimal executable detection and device listing.
- `device/`: converts ADB properties and shell output into `DeviceInfo`.
- `magisk/`: root/Magisk detection and developer module operations.
- `configuration/`: validated JSON configuration and file backups.
- `backup/`: device-state metadata snapshots and serial verification.
- `diagnostics/`: JSON diagnostic reports.
- `logging_tool/`: JSON-lines event logging. Runtime output goes under `logs/`.
- `cli/`: argparse command wiring and human-readable errors.
- `modules/`: the harmless educational test module.
- `tests/`: offline tests using fake runners and temporary directories.

Subprocess access is isolated in `AdbManager`, so tests can inject a callable runner. Device operations select a serial explicitly when more than one usable device is connected.
