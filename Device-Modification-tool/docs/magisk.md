# Magisk integration

Magisk operations require a developer-owned test phone with Magisk already installed. Root availability is detected with `id`; Magisk availability is detected with `command -v magisk`.

Build the educational module:

```powershell
.\scripts\build-test-module.ps1
```

Install and inspect it:

```powershell
device-tool --serial SERIAL magisk status
device-tool --serial SERIAL magisk install modules\device-tool-test.zip
device-tool --serial SERIAL reboot
device-tool --serial SERIAL magisk remove device_tool_test
```

The current Phase 1 module writes `/data/local/tmp/device-tool-test-module.txt` at boot and logs under its module directory. Verify the file and module state after reboot. The module is intentionally not a security bypass and does not modify protected system files.
