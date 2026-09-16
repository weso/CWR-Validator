# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import pytest

VALIDATOR_ROOT = Path(__file__).resolve().parents[1]
LIBRARIES_ROOT = VALIDATOR_ROOT.parent


@pytest.fixture
def sibling_library_paths(monkeypatch):
    v21 = LIBRARIES_ROOT / "CWR_LIBRARY_V2.1"
    v22 = LIBRARIES_ROOT / "CWR_LIBRARY_V2.2"
    if not (v21 / "cwr" / "parser" / "decoder" / "file.py").is_file():
        pytest.skip("CWR_LIBRARY_V2.1 submodule not present")
    if not (v22 / "cwr" / "parser" / "decoder" / "file.py").is_file():
        pytest.skip("CWR_LIBRARY_V2.2 submodule not present")
    monkeypatch.setenv("CWR_LIBRARY_V21_PATH", str(v21))
    monkeypatch.setenv("CWR_LIBRARY_V22_PATH", str(v22))
    return v21, v22


@pytest.fixture
def v21_example_path():
    path = LIBRARIES_ROOT / "CWR_LIBRARY_V2.2" / "tests" / "examples" / "nwrexample2.V21"
    if not path.is_file():
        pytest.skip("v2.1 example file not found")
    return path


@pytest.fixture
def v22_example_path():
    path = LIBRARIES_ROOT / "CWR_LIBRARY_V2.2" / "tests" / "examples" / "demo_cwr_cleaned.v22"
    if not path.is_file():
        pytest.skip("v2.2 example file not found")
    return path
