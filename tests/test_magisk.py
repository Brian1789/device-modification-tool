from pathlib import Path

import pytest

from magisk import MagiskError, MagiskManager


def test_module_install_requires_local_zip(tmp_path):
    class Adb: pass
    manager = MagiskManager(Adb())
    with pytest.raises(MagiskError):
        manager.install("ABC", tmp_path / "missing.zip")
    non_zip = tmp_path / "module.txt"
    non_zip.write_text("x", encoding="utf-8")
    with pytest.raises(MagiskError):
        manager.install("ABC", non_zip)


def test_module_tree_contains_required_files():
    root = Path(__file__).parents[1] / "modules" / "device-tool-test"
    assert (root / "module.prop").exists()
    assert (root / "service.sh").exists()
    assert (root / "uninstall.sh").exists()
