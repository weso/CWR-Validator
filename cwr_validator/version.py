# -*- coding: utf-8 -*-
"""CWR version detection from filenames and CLI overrides."""

from __future__ import annotations

from pathlib import Path

EXTENSION_VERSIONS = {
    ".V21": "2.1",
    ".V22": "2.2",
}


class VersionError(Exception):
    """Raised when a file version cannot be determined or conflicts."""


def normalize_version(value: str) -> str:
    cleaned = value.strip()
    if cleaned in ("2.1", "2.2"):
        return cleaned
    raise VersionError(f"Unsupported version {value!r}; use 2.1 or 2.2")


def version_from_extension(path: Path) -> str | None:
    suffix = path.suffix.upper()
    return EXTENSION_VERSIONS.get(suffix)


def resolve_file_version(path: Path, forced_version: str | None) -> str:
    detected = version_from_extension(path)
    if forced_version:
        forced = normalize_version(forced_version)
        if detected and detected != forced:
            raise VersionError(
                f"{path.name}: extension implies {detected} but "
                f"--version {forced} was requested"
            )
        return forced
    if detected:
        return detected
    raise VersionError(
        f"{path.name}: cannot detect CWR version from extension; "
        "use --version 2.1 or --version 2.2"
    )
