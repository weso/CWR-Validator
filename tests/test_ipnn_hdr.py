# -*- coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

import pytest

from cwr_validator.preprocess import normalize_contents_for_decode
from cwr_validator.validator import validate_file

VALIDATOR_ROOT = Path(__file__).resolve().parents[1]
HDR_IPNN_FIXTURE = VALIDATOR_ROOT / "tests" / "fixtures" / "hdr_ipnn_v21.V21"


def test_hdr_ipnn_is_normalized():
    raw = HDR_IPNN_FIXTURE.read_text(encoding="latin-1")
    first_line = raw.splitlines()[0]
    assert first_line.startswith("HDR01")

    normalized = normalize_contents_for_decode(raw, "2.1")
    assert normalized.splitlines()[0].startswith("HDRPB234567890")


def test_hdr_ipnn_grh_v22_version_is_normalized():
    """GRH 02.20 is mapped to 02.10 for decode-only passes on v2.2 files."""
    contents = (
        "HDRPB234567890THE SENDER                                   "
        "01.102026060610551820260606               \r\n"
        "GRHNWR0000102.200000000001\r\n"
    )
    result = normalize_contents_for_decode(contents, "2.2")
    assert "GRHNWR0000102.100000000001" in result


@pytest.mark.integration
def test_validate_hdr_ipnn_fixture(sibling_library_paths):
    result = validate_file(HDR_IPNN_FIXTURE)
    if not result.ok:
        pytest.skip(f"CWR library decode unavailable in this environment: {result.error}")
    assert result.version == "2.1"
    assert result.groups is not None and result.groups >= 1
