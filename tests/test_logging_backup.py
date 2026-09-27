import json

from backup import BackupManager
from logging_tool import StructuredLogger


def test_structured_logger_writes_expected_fields(tmp_path):
    path = tmp_path / "logs" / "application.log"
    StructuredLogger(path).event("test", "ok", device="ABC", secret_should_not_be_used="ignored")
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["operation"] == "test"
    assert record["device"] == "ABC"
    assert "timestamp" in record


def test_backup_metadata_and_verify(tmp_path):
    class Collector:
        def collect(self, serial=None):
            class Info:
                serial = "ABC"
                def to_dict(self): return {"serial": self.serial, "model": "Test"}
            return Info()

    manager = BackupManager(Collector(), tmp_path / "backups")
    path = manager.create()
    assert manager.verify(path)
    assert manager.restore(path)["device"]["serial"] == "ABC"
