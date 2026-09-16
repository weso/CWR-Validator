# -*- coding: utf-8 -*-
"""Orchestrate CWR file validation via isolated subprocess workers."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from cwr_validator.library_paths import (
    LibraryPathError,
    LibraryPaths,
    library_path_for_version,
    resolve_library_paths,
    validate_library_path,
)
from cwr_validator.version import VersionError, resolve_file_version


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    version: str
    file: str
    groups: int | None = None
    transactions: int | None = None
    error: str | None = None
    error_type: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> ValidationResult:
        return cls(
            ok=bool(data.get("ok")),
            version=data.get("version", ""),
            file=data.get("file", ""),
            groups=data.get("groups"),
            transactions=data.get("transactions"),
            error=data.get("error"),
            error_type=data.get("error_type"),
        )


def _worker_command(library_path: Path, version: str, file_path: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "cwr_validator.worker",
        "--library-path",
        str(library_path),
        "--version",
        version,
        str(file_path),
    ]


def validate_file(
    file_path: Path,
    *,
    forced_version: str | None = None,
    paths: LibraryPaths | None = None,
) -> ValidationResult:
    """Validate one CWR file using the matching local library checkout."""
    file_path = file_path.resolve()
    if not file_path.is_file():
        return ValidationResult(
            ok=False,
            version=forced_version or "",
            file=str(file_path),
            error=f"File not found: {file_path}",
            error_type="FileNotFoundError",
        )

    try:
        version = resolve_file_version(file_path, forced_version)
        lib_paths = paths or resolve_library_paths()
        library_path = library_path_for_version(lib_paths, version)
        validate_library_path(library_path, version)
    except (VersionError, LibraryPathError) as exc:
        return ValidationResult(
            ok=False,
            version=forced_version or "",
            file=str(file_path),
            error=str(exc),
            error_type=type(exc).__name__,
        )

    proc = subprocess.run(
        _worker_command(library_path, version, file_path),
        capture_output=True,
        text=True,
        cwd=str(Path(__file__).resolve().parent.parent),
    )

    if proc.returncode not in (0, 1):
        return ValidationResult(
            ok=False,
            version=version,
            file=str(file_path),
            error=proc.stderr.strip() or f"Worker exited with code {proc.returncode}",
            error_type="WorkerError",
        )

    try:
        payload = json.loads(proc.stdout.strip() or "{}")
    except json.JSONDecodeError as exc:
        return ValidationResult(
            ok=False,
            version=version,
            file=str(file_path),
            error=f"Invalid worker output: {exc}",
            error_type="JSONDecodeError",
        )

    return ValidationResult.from_dict(payload)


def validate_files(
    file_paths: list[Path],
    *,
    forced_version: str | None = None,
    paths: LibraryPaths | None = None,
) -> list[ValidationResult]:
    """Validate multiple CWR files (one subprocess per file)."""
    lib_paths = paths
    results: list[ValidationResult] = []
    for file_path in file_paths:
        results.append(
            validate_file(file_path, forced_version=forced_version, paths=lib_paths)
        )
        if lib_paths is None:
            lib_paths = resolve_library_paths()
    return results
