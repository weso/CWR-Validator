# -*- encoding: utf-8 -*-
"""
Utilities functions.
"""

__author__ = 'Borja Garrido Bear'
__license__ = 'MIT'
__version__ = '0.0.0'
__status__ = 'Development'


def enum(**enums):
    return type('Enum', (), enums)
