# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from unittest.mock import MagicMock

from cwr_validator.cli import main


def test_cli_json_success(monkeypatch, sibling_library_paths, tmp_path, capsys):
    file_path = tmp_path / "good.V21"
    file_path.write_text("HDR", encoding="latin-1")

    payload = {
        "ok": True,
        "version": "2.1",
        "file": str(file_path.resolve()),
        "groups": 1,
        "transactions": 1,
    }

    def _run(cmd, **kwargs):
        result = MagicMock()
        result.returncode = 0
        result.stdout = json.dumps(payload)
        result.stderr = ""
        return result

    monkeypatch.setattr("cwr_validator.validator.subprocess.run", _run)

    code = main([str(file_path), "--json"])
    assert code == 0
    out = json.loads(capsys.readouterr().out)
    assert out[0]["ok"] is True


def test_cli_failure_exit_code(sibling_library_paths, tmp_path, capsys):
    bad = tmp_path / "bad.V21"
    bad.write_text("HDR truncated", encoding="latin-1")
    code = main([str(bad)])
    assert code == 1
    assert "FAIL" in capsys.readouterr().out


def test_cli_quiet_hides_pass(monkeypatch, sibling_library_paths, tmp_path, capsys):
    file_path = tmp_path / "good.V21"
    file_path.write_text("HDR", encoding="latin-1")

    payload = {
        "ok": True,
        "version": "2.1",
        "file": str(file_path.resolve()),
        "groups": 1,
        "transactions": 1,
    }

    def _run(cmd, **kwargs):
        result = MagicMock()
        result.returncode = 0
        result.stdout = json.dumps(payload)
        result.stderr = ""
        return result

    monkeypatch.setattr("cwr_validator.validator.subprocess.run", _run)

    code = main([str(file_path), "-q"])
    assert code == 0
    assert capsys.readouterr().out == ""
