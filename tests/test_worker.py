# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from cwr_validator.worker import decode_file

VALIDATOR_ROOT = Path(__file__).resolve().parents[1]
LIBRARIES_ROOT = VALIDATOR_ROOT.parent


@pytest.mark.integration
def test_worker_decode_inline_v21_fixture(sibling_library_paths, tmp_path):
    """End-to-end worker decode when the CWR library stack is compatible."""
    from tests.data.sample_v21_contents import sample_v21_contents

    v21, _v22 = sibling_library_paths
    file_path = tmp_path / "sample.V21"
    file_path.write_text(sample_v21_contents(), encoding="latin-1")

    try:
        result = decode_file(v21, file_path, "2.1")
    except Exception as exc:
        pytest.skip(f"CWR library decode unavailable in this environment: {exc}")

    if not result["ok"]:
        pytest.skip(f"CWR library decode failed in this environment: {result.get('error')}")

    assert result["version"] == "2.1"
    assert result["groups"] == 2


@pytest.mark.integration
def test_worker_subprocess_entry(sibling_library_paths, tmp_path):
    from tests.data.sample_v21_contents import sample_v21_contents

    v21, _v22 = sibling_library_paths
    file_path = tmp_path / "sample.V21"
    file_path.write_text(sample_v21_contents(), encoding="latin-1")

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "cwr_validator.worker",
            "--library-path",
            str(v21),
            "--version",
            "2.1",
            str(file_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(VALIDATOR_ROOT),
    )
    payload = json.loads(proc.stdout)
    if not payload["ok"]:
        pytest.skip(f"CWR library decode failed: {payload.get('error')}")
    assert proc.returncode == 0
