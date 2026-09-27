# Windows setup

Install Git, Python 3.x, and Android SDK Platform-Tools. Android Studio is not required. Add the Platform-Tools directory containing `adb.exe` and `fastboot.exe` to the user `PATH`, then open a new PowerShell window.

```powershell
py -3 --version
adb version
fastboot --version
cd C:\path\to\Device-Modification-tool
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -e .
py -3 -m pip install -r requirements-dev.txt
```

If PowerShell blocks activation, use `py -3 -m pip install -e .` without activation, or ask an administrator to set an execution policy appropriate for the machine.

On the phone, enable Developer options and USB debugging. Connect with a known-good data cable, accept the RSA dialog, and run `device-tool devices`.
