# -*- coding: utf-8 -*-
"""Resolve configurable paths to local CWR DataApi library checkouts."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from data_validator.accessor import CWRValidatorConfiguration

VALIDATOR_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_V21_REL = Path("..") / "CWR_LIBRARY_V2.1"
DEFAULT_V22_REL = Path("..") / "CWR_LIBRARY_V2.2"
DECODER_MARKER = Path("cwr") / "parser" / "decoder" / "file.py"

ENV_V21 = "CWR_LIBRARY_V21_PATH"
ENV_V22 = "CWR_LIBRARY_V22_PATH"
PROP_V21 = "library.v21.path"
PROP_V22 = "library.v22.path"


@dataclass(frozen=True)
class LibraryPaths:
    """Absolute paths to v2.1 and v2.2 CWR library roots."""

    v21: Path
    v22: Path


class LibraryPathError(Exception):
    """Raised when a configured library path is missing or invalid."""


def _resolve_raw(version: str, raw: str | None, default_rel: Path) -> Path:
    if raw:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            path = (VALIDATOR_ROOT / path).resolve()
        else:
            path = path.resolve()
    else:
        path = (VALIDATOR_ROOT / default_rel).resolve()
    return path


def _load_properties() -> dict[str, str]:
    return CWRValidatorConfiguration().get_config()


def resolve_library_paths() -> LibraryPaths:
    """Return validated absolute paths for both CWR library versions.

    Precedence per version: environment variable, config.properties, default
    sibling path under LIBRARIES/.
    """
    props = _load_properties()
    v21 = _resolve_raw(
        "2.1",
        os.environ.get(ENV_V21) or props.get(PROP_V21) or None,
        DEFAULT_V21_REL,
    )
    v22 = _resolve_raw(
        "2.2",
        os.environ.get(ENV_V22) or props.get(PROP_V22) or None,
        DEFAULT_V22_REL,
    )
    return LibraryPaths(v21=v21, v22=v22)


def library_path_for_version(paths: LibraryPaths, version: str) -> Path:
    if version == "2.1":
        return paths.v21
    if version == "2.2":
        return paths.v22
    raise LibraryPathError(f"Unsupported CWR version: {version!r}")


def validate_library_path(path: Path, version: str) -> None:
    if not path.is_dir():
        raise LibraryPathError(
            f"CWR {version} library path does not exist: {path}"
        )
    marker = path / DECODER_MARKER
    if not marker.is_file():
        raise LibraryPathError(
            f"CWR {version} library path is missing {DECODER_MARKER}: {path}"
        )


def validate_library_paths(paths: LibraryPaths) -> None:
    validate_library_path(paths.v21, "2.1")
    validate_library_path(paths.v22, "2.2")
