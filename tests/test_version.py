# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import pytest

from cwr_validator.version import VersionError, resolve_file_version, version_from_extension


def test_version_from_extension():
    assert version_from_extension(Path("file.V21")) == "2.1"
    assert version_from_extension(Path("file.V22")) == "2.2"
    assert version_from_extension(Path("file.v22")) == "2.2"
    assert version_from_extension(Path("file.txt")) is None


def test_resolve_file_version_from_extension():
    assert resolve_file_version(Path("CW12012311_22.V21"), None) == "2.1"
    assert resolve_file_version(Path("CW251600001_707.V22"), None) == "2.2"


def test_forced_version_matches_extension():
    assert resolve_file_version(Path("a.V21"), "2.1") == "2.1"


def test_forced_version_conflicts_with_extension():
    with pytest.raises(VersionError, match="extension implies"):
        resolve_file_version(Path("a.V21"), "2.2")


def test_missing_extension_requires_forced_version():
    with pytest.raises(VersionError, match="cannot detect"):
        resolve_file_version(Path("noext"), None)
