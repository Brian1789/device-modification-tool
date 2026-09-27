from types import SimpleNamespace

from adb import AdbManager


class FakeRunner:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.commands = []

    def __call__(self, command, **kwargs):
        self.commands.append(command)
        return SimpleNamespace(stdout=self.stdout, stderr=self.stderr, returncode=self.returncode)


def test_list_devices_and_properties():
    runner = FakeRunner("List of devices attached\nABC123\tdevice product:test model:Pixel\nOFF\toffline\n")
    adb = AdbManager(runner=runner)
    devices = adb.list_devices()
    assert devices[0].serial == "ABC123"
    assert devices[0].state == "device"
    assert devices[1].state == "offline"

    props_runner = FakeRunner("[ro.product.model]: [Test Phone]\n[ro.build.version.sdk]: [35]\n")
    props = AdbManager(runner=props_runner).get_properties("ABC123")
    assert props == {"ro.product.model": "Test Phone", "ro.build.version.sdk": "35"}


def test_shell_failure_reports_error():
    runner = FakeRunner(stderr="error: device unauthorized", returncode=1)
    adb = AdbManager(runner=runner)
    try:
        adb.shell("id", "ABC123")
    except Exception as exc:
        assert "unauthorized" in str(exc)
    else:
        raise AssertionError("expected shell failure")
