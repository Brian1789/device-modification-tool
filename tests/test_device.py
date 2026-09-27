from adb import CommandResult, DeviceRecord
from device import DeviceInfoCollector


class FakeAdb:
    def list_devices(self):
        return [DeviceRecord("ABC", "device")]

    def get_properties(self, serial):
        return {
            "ro.product.manufacturer": "Acme",
            "ro.product.model": "Test",
            "ro.build.version.release": "14",
            "ro.build.version.sdk": "34",
            "ro.product.cpu.abi": "arm64-v8a",
        }

    def shell(self, command, serial, timeout=None):
        values = {"uname -a": "Linux test", "wm size": "Physical size: 1080x2400", "cat /proc/meminfo | head -n 3": "MemTotal: 8 MB", "df -h /data": "/data 10G 2G 8G", "getprop ro.boot.verifiedbootstate": "green", "id": "uid=2000(shell)", "command -v magisk": "/sbin/magisk"}
        return CommandResult(["adb"], 0, values.get(command, ""), "")


def test_collect_device_information():
    info = DeviceInfoCollector(FakeAdb()).collect()
    assert info.model == "Test"
    assert info.android_version == "14"
    assert info.architecture == "arm64-v8a"
    assert info.magisk_installed is True
    assert info.root_available is False
