# Android Device Modification Tool

A lightweight Python toolkit for managing a physical Android test device over ADB and Fastboot. It is designed for an 8 GB Windows laptop and does not require Android Studio, an emulator, Docker, or a virtual machine.

## Features

- `device-tool devices`, `status`, `info`, `shell`, and `diagnostics`
- Structured ADB execution with timeouts and unauthorized/offline errors
- Device properties, architecture, kernel, screen, memory, storage, root, and Magisk detection
- JSON configuration with explicit backup and restore
- Device-state backup metadata and verification
- Developer-owned Magisk module install, enable/disable, listing, and removal primitives
- JSON-lines application logging without credential fields
- Mock-based tests that run without a phone

## Quick start on Windows

1. Install Python 3.10+, Git, and Android SDK Platform-Tools. Add the Platform-Tools directory to `PATH`.
2. Enable Developer options and USB debugging on a physical test device. Connect it and accept the RSA prompt.
3. Create an environment and install the project:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
py -3 -m pip install -r requirements-dev.txt
```

4. Run offline tests:

```powershell
py -3 -m pytest -q
```

5. Inspect the device:

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
