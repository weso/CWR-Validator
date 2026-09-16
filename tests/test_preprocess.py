# -*- coding: utf-8 -*-

from __future__ import annotations

from cwr_validator.preprocess import normalize_contents_for_decode


def test_hdr_ipnn_workaround_rewrites_sender_type():
    hdr = (
        "HDR01234567890THE SENDER                                   "
        "01.102026060610551820260606               \r\n"
        "GRHNWR0000102.200000000001\r\n"
    )
    result = normalize_contents_for_decode(hdr, "2.2")
    assert result.startswith("HDRPB234567890THE SENDER")
    assert "GRHNWR0000102.100000000001" in result


def test_hdr_standard_sender_type_unchanged():
    hdr = "HDRPB226144593AGENCIA GRUPO MUSICAL                        01.102013080902591120130809\r\n"
    assert normalize_contents_for_decode(hdr, "2.1") == hdr


def test_hdr_ascii_character_set_is_blanked_for_decode():
    hdr = (
        "HDRPB123456789ACME PUBLISHING                              "
        "01.102026062917593820260629ASCII          2.2\r\n"
    )
    result = normalize_contents_for_decode(hdr, "2.2")
    assert "ASCII" not in result.splitlines()[0]
    assert result.splitlines()[0].endswith("2.2")


def test_hdr_non_ascii_character_set_unchanged():
    hdr = (
        "HDRPB123456789ACME PUBLISHING                              "
        "01.102026062917593820260629Big5           2.2\r\n"
    )
    assert normalize_contents_for_decode(hdr, "2.2") == hdr
