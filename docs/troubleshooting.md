# Troubleshooting

**ADB is not installed:** Install Platform-Tools and reopen PowerShell so `PATH` is refreshed.

**No device or `unauthorized`:** Unlock the phone, enable USB debugging, reconnect the cable, and accept the RSA prompt. `adb kill-server; adb start-server` can refresh the connection.

**`offline`:** Try another data cable/USB port, then reconnect and restart ADB.

**Multiple devices:** Pass `--serial SERIAL` to every device command.

**Root or Magisk unavailable:** The phone may not be rooted, Magisk may not be installed, or the shell may not have been granted root. Magisk commands are expected to fail in that state.

**PowerShell cannot run `build-test-module.ps1`:** Run the script from a trusted local checkout or use `Compress-Archive` manually. Do not lower system policy globally just for this project.

**Device changes fail:** Review `logs/application.log` and device-side logs. The project never logs passwords, tokens, private keys, or authentication secrets.
