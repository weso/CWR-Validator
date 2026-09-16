# -*- coding: utf-8 -*-
"""Normalize CWR file contents before handing them to the DataApi decoder."""

from __future__ import annotations

import re

# CWR 2.1 Rev 8 / 2.2 Rev 2: when the sender IPNN exceeds nine digits, the leading
# two digits occupy HDR Sender Type (positions 4-5) and the remaining nine occupy
# Sender ID (positions 6-14). Legacy DataApi grammars only accept PB/SO/AA/WR in
# Sender Type, so the validator rewrites numeric prefixes to PB for decode only.
_HDR_IPNN_SENDER_TYPE = re.compile(r"^(HDR)(\d{2})(\d{9})")
_GRH_V22_VERSION = re.compile(r"^(GRH.{8})02\.20")

# CISAC positions 87-101 (0-based 86:101): optional Character Set on HDR.
_HDR_CHARACTER_SET_START = 86
_HDR_CHARACTER_SET_SIZE = 15


def normalize_contents_for_decode(contents: str, version: str) -> str:
    """Return file contents adjusted for known library grammar gaps."""
    lines = contents.splitlines(keepends=True)
    if not lines:
        return contents

    normalized: list[str] = []
    for index, line in enumerate(lines):
        body = line.rstrip("\r\n")
        ending = line[len(body):]
        if index == 0 and body.startswith("HDR"):
            body = _normalize_hdr_character_set_ascii(_normalize_hdr_ipnn(body))
        elif version == "2.2" and body.startswith("GRH"):
            body = _GRH_V22_VERSION.sub(r"\g<1>02.10", body)
        normalized.append(body + ending)
    return "".join(normalized)


def _normalize_hdr_ipnn(hdr_line: str) -> str:
    match = _HDR_IPNN_SENDER_TYPE.match(hdr_line)
    if not match:
        return hdr_line
    prefix, _ipnn_leading, ipnn_tail = match.groups()
    return f"{prefix}PB{ipnn_tail}{hdr_line[14:]}"


def _normalize_hdr_character_set_ascii(hdr_line: str) -> str:
    """Blank HDR Character Set when submitters wrote ASCII (decode-only shim).

    CISAC defines the field for non-ASCII sets only. Many generators omit
    the field for ASCII-only files; older/third-party files may still carry
    ``ASCII`` there. The DataApi charset grammar accepts Big5, GB, and Unicode
    codes but not that literal, so treat ASCII the same as an omitted field.
    """
    end = _HDR_CHARACTER_SET_START + _HDR_CHARACTER_SET_SIZE
    if len(hdr_line) < end:
        return hdr_line
    charset = hdr_line[_HDR_CHARACTER_SET_START:end]
    if charset.strip().upper() != "ASCII":
        return hdr_line
    return (
        hdr_line[:_HDR_CHARACTER_SET_START]
        + (" " * _HDR_CHARACTER_SET_SIZE)
        + hdr_line[end:]
    )
