# -*- coding: utf-8 -*-
"""
CWR file validator CLI.

Validates .V21 and .V22 files by parsing them through configurable local
checkouts of the CWR DataApi library (v2.1 and v2.2).
"""

from cwr_validator.validator import ValidationResult, validate_file, validate_files

__version__ = "1.0.0"
__license__ = "MIT"

__all__ = ["ValidationResult", "validate_file", "validate_files", "__version__"]
