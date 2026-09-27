# Testing

The unit suite can run without an emulator:

```powershell
py -3 -m pytest -q
```

Coverage includes ADB device parsing, properties, unauthorized errors, device info collection, configuration validation and rollback, structured logging, backup metadata, module input validation, and required module files.

Emulator smoke checks require Android Studio, a configured virtualization provider, and a running AVD. The target serial must start with `emulator-`:

```powershell
device-tool devices
device-tool info --serial SERIAL
device-tool diagnostics --serial SERIAL --output diagnostics\smoke.json
device-tool backup --serial SERIAL
```

Physical USB devices are not part of the supported test configuration.
