import json

import pytest

from configuration import ConfigError, ConfigurationManager


def test_configuration_load_validate_backup_restore(tmp_path):
    manager = ConfigurationManager(tmp_path / "config")
    manager.default_file.parent.mkdir()
    manager.default_file.write_text(json.dumps({"profile": "test", "settings": {"x": 1}}), encoding="utf-8")
    assert manager.load()["profile"] == "test"
    backup = manager.backup()
    manager.default_file.write_text(json.dumps({"profile": "changed"}), encoding="utf-8")
    manager.restore(backup)
    assert manager.load()["profile"] == "test"


def test_invalid_configuration_is_rejected(tmp_path):
    manager = ConfigurationManager(tmp_path / "config")
    manager.default_file.parent.mkdir()
    manager.default_file.write_text("[]", encoding="utf-8")
    with pytest.raises(ConfigError):
        manager.load()
