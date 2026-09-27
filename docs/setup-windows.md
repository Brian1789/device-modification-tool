# Windows setup

Install Git, Python 3.x, and Android Studio. In the Android Studio SDK Manager, install Android SDK Platform-Tools, Android SDK tools, and Android Emulator. Android Studio is required for the supported workflow.

Enable CPU virtualization in firmware and configure a virtualization-capable Windows VM provider such as WHPX or Hyper-V. In Android Studio, create an Android Virtual Device (AVD) and start it before using this project. The supported target is an Android Studio emulator; physical USB devices are not supported.

```powershell
py -3 --version
adb version
fastboot --version
adb devices
cd C:\path\to\Device-Modification-tool
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
py -3 -m pip install -r requirements-dev.txt
```

If PowerShell blocks activation, use `py -3 -m pip install -e .` without activation, or ask an administrator to set an execution policy appropriate for the machine.

`adb devices` must show an `emulator-` serial in the `device` state. Start the AVD from Android Studio if it is missing or offline, then run `device-tool devices`.
