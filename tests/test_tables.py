# -*- coding: utf-8 -*-

from cwr_validator.tables import EXTRA_SOCIETY_CODES


def test_alltrack_society_is_extended():
    assert "786" in EXTRA_SOCIETY_CODES
