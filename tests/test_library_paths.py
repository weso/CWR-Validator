# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import pytest

from cwr_validator.library_paths import (
    LibraryPathError,
    LibraryPaths,
    resolve_library_paths,
    validate_library_path,
)


def test_default_paths_resolve_to_sibling_libraries():
    paths = resolve_library_paths()
    assert paths.v21.name == "CWR_LIBRARY_V2.1"
    assert paths.v22.name == "CWR_LIBRARY_V2.2"


def test_env_overrides_properties(monkeypatch, tmp_path):
    custom = tmp_path / "custom_lib"
    custom.mkdir()
    (custom / "cwr").mkdir(parents=True)
    (custom / "cwr" / "parser").mkdir(parents=True)
    (custom / "cwr" / "parser" / "decoder").mkdir(parents=True)
    (custom / "cwr" / "parser" / "decoder" / "file.py").write_text("# stub")

    monkeypatch.setenv("CWR_LIBRARY_V21_PATH", str(custom))
    paths = resolve_library_paths()
    assert paths.v21 == custom.resolve()


def test_validate_library_path_missing_dir():
    with pytest.raises(LibraryPathError, match="does not exist"):
        validate_library_path(Path("/nonexistent/cwr-lib"), "2.1")


def test_validate_library_paths_with_siblings(sibling_library_paths):
    v21, v22 = sibling_library_paths
    paths = LibraryPaths(v21=v21, v22=v22)
    validate_library_path(paths.v21, "2.1")
    validate_library_path(paths.v22, "2.2")
