# Testing

The suite is designed to run without Android hardware:

```powershell
py -3 -m pytest -q
```

Coverage includes ADB device parsing, properties, unauthorized errors, device info collection, configuration validation and rollback, structured logging, backup metadata, module input validation, and required module files.

Hardware smoke checks should be performed only on a disposable developer test device:

```powershell
device-tool devices
device-tool info --serial SERIAL
device-tool diagnostics --serial SERIAL --output diagnostics\smoke.json
device-tool backup --serial SERIAL
```
