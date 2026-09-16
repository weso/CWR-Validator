# -*- coding: utf-8 -*-
"""Subprocess worker: decode one CWR file with a single library on sys.path."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


from cwr_validator.preprocess import normalize_contents_for_decode


def _count_transactions(transmission) -> int:
    total = 0
    for group in transmission.groups:
        for transaction in group.transactions:
            total += len(transaction)
    return total


def decode_file(library_path: Path, file_path: Path, version: str) -> dict:
    sys.path.insert(0, str(library_path))
    from cwr_validator.tables import patch_cwr_tables

    patch_cwr_tables()
    from cwr.parser.decoder.file import default_file_decoder

    filename = file_path.name
    raw = file_path.read_bytes()
    try:
        contents = raw.decode("utf-8")
    except UnicodeDecodeError:
        contents = raw.decode("latin-1")
    contents = normalize_contents_for_decode(contents, version)
    decoder = default_file_decoder()
    cwr_file = decoder.decode({"filename": filename, "contents": contents})
    transmission = cwr_file.transmission
    return {
        "ok": True,
        "version": version,
        "file": str(file_path),
        "groups": len(transmission.groups),
        "transactions": _count_transactions(transmission),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CWR decode worker (internal)")
    parser.add_argument("--library-path", required=True)
    parser.add_argument("--version", required=True, choices=("2.1", "2.2"))
    parser.add_argument("file", type=Path)
    args = parser.parse_args(argv)

    library_path = Path(args.library_path).resolve()
    file_path = args.file.resolve()

    try:
        result = decode_file(library_path, file_path, args.version)
    except Exception as exc:
        result = {
            "ok": False,
            "version": args.version,
            "file": str(file_path),
            "error": str(exc),
            "error_type": type(exc).__name__,
        }

    print(json.dumps(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
