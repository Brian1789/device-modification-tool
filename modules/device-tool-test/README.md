# Educational test module

This developer-owned module creates `/data/local/tmp/device-tool-test-module.txt` at boot and records a line in its module directory log. It does not bypass security controls or modify protected system files.

Zip the contents of this directory, preserving `module.prop`, `service.sh`, and `uninstall.sh` at the ZIP root, then install it with `device-tool magisk install path\to\module.zip`.
