# Android Device Modification Tool

A lightweight Python toolkit for managing an Android Studio emulator over ADB and Fastboot. Android Studio, an Android Virtual Device (AVD), and a virtualization-capable VM are required. Physical USB devices are not supported by the documented workflow.

## Features

- `device-tool devices`, `status`, `info`, `shell`, and `diagnostics`
- Structured ADB execution with timeouts and unauthorized/offline errors
- Device properties, architecture, kernel, screen, memory, storage, root, and Magisk detection
- JSON configuration with explicit backup and restore
- Device-state backup metadata and verification
- Developer-owned Magisk module install, enable/disable, listing, and removal primitives
- JSON-lines application logging without credential fields
- Mock-based unit tests plus emulator-backed integration checks

## Quick start on Windows

1. Install Python 3.10+, Git, and Android Studio with the Android SDK, SDK Platform-Tools, and Android Emulator components.
2. Enable hardware virtualization in firmware and configure the Android Emulator to use the host virtualization provider (WHPX or Hyper-V on Windows).
3. In Android Studio, create and start an Android Virtual Device (AVD). Leave the emulator running before using this tool.
4. Verify that the emulator is visible to ADB:

```powershell
adb devices
```

The target must appear with an `emulator-` serial. Physical USB devices are outside the supported configuration.

5. Create an environment and install the project:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
py -3 -m pip install -r requirements-dev.txt
```

6. Run unit tests:

```powershell
py -3 -m pytest -q
```

7. Inspect the running emulator:

```powershell
device-tool devices
device-tool status
device-tool info --json
device-tool diagnostics --output diagnostics\device.json
```

For an uninstalled checkout, use `py -3 -m cli.main ...` instead of `device-tool ...`.

## Safety model

The toolkit targets developer-owned test devices. It does not unlock bootloaders, bypass platform security, evade anti-abuse systems, or include third-party modules. Backup and verification are explicit. `restore` validates backup metadata; it does not silently flash partitions or overwrite device data.

See [docs/setup-windows.md](docs/setup-windows.md), [docs/architecture.md](docs/architecture.md), and [docs/troubleshooting.md](docs/troubleshooting.md).
