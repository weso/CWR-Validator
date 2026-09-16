# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from cwr_validator.library_paths import LibraryPaths
from cwr_validator.validator import validate_file


def _mock_subprocess_run_factory(responses: dict[str, dict]):
    def _run(cmd, **kwargs):
        file_arg = cmd[-1]
        payload = responses.get(file_arg, {"ok": False, "error": "missing mock"})
        result = MagicMock()
        result.returncode = 0 if payload.get("ok") else 1
        result.stdout = json.dumps(payload)
        result.stderr = ""
        return result

    return _run


def test_validate_file_success(monkeypatch, sibling_library_paths, tmp_path):
    v21, v22 = sibling_library_paths
    paths = LibraryPaths(v21=v21, v22=v22)
    file_path = tmp_path / "good.V21"
    file_path.write_text("HDR", encoding="latin-1")

    payload = {
        "ok": True,
        "version": "2.1",
        "file": str(file_path),
        "groups": 2,
        "transactions": 4,
    }
    monkeypatch.setattr(
        "cwr_validator.validator.subprocess.run",
        _mock_subprocess_run_factory({str(file_path.resolve()): payload}),
    )

    result = validate_file(file_path, paths=paths)
    assert result.ok
    assert result.version == "2.1"
    assert result.groups == 2
    assert result.transactions == 4


def test_validate_truncated_file_fails(sibling_library_paths, tmp_path):
    bad = tmp_path / "bad.V21"
    bad.write_text("HDR truncated", encoding="latin-1")
    result = validate_file(bad)
    assert not result.ok
    assert result.error


def test_validate_missing_file(sibling_library_paths):
    result = validate_file(Path("/nonexistent/file.V21"))
    assert not result.ok
    assert result.error_type == "FileNotFoundError"


def test_validate_version_mismatch(sibling_library_paths, tmp_path):
    file_path = tmp_path / "x.V22"
    file_path.write_text("HDR", encoding="latin-1")
    result = validate_file(file_path, forced_version="2.1")
    assert not result.ok
    assert result.error_type == "VersionError"
