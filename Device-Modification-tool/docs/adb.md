# ADB operations

Useful commands:

```powershell
device-tool devices
device-tool --serial SERIAL info
device-tool --serial SERIAL shell "getprop ro.build.version.release"
device-tool --serial SERIAL backup
device-tool --serial SERIAL diagnostics --output diagnostics\SERIAL.json
```

`AdbManager` returns structured `CommandResult` values with command, return code, stdout, and stderr. Shell commands have a timeout. Unauthorized and offline errors are converted to `AdbError` with an actionable message.

Do not use `shell` for destructive commands unless you understand the device effect. The toolkit intentionally does not expose arbitrary flashing or bootloader-unlock workflows.
