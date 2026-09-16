# -*- coding: utf-8 -*-
"""Extend DataApi lookup tables with societies the vendored lists omit."""

from __future__ import annotations

# Alltrack (CISAC 786) is not in weso/CWR-DataApi cwr_society_code.csv (max 310).
EXTRA_SOCIETY_CODES = ("786",)

_patched = False


def patch_cwr_tables() -> None:
    """Append EXTRA_SOCIETY_CODES to CWRTables society_code before grammar load.

    Must run after the DataApi library is on sys.path and before the CWR
    decoder is imported, so lookup fields accept Alltrack PR affiliations.
    """
    global _patched
    if _patched:
        return

    from data_cwr.accessor import CWRTables

    original = CWRTables.get_data

    def get_data(self, file_id):
        data = original(self, file_id)
        if file_id == "society_code":
            for code in EXTRA_SOCIETY_CODES:
                if code not in data:
                    data.append(code)
        return data

    CWRTables.get_data = get_data
    _patched = True
