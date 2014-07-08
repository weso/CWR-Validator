__author__ = 'Borja'
from validator.cwr_utils import regex


class AviKey(object):
    SOCIETY_CODE = regex.get_numeric_regex(3, True)
    NUMBER = regex.get_ascii_regex(15, True)

    REGEX = '{0}{1}'.format(SOCIETY_CODE, NUMBER)

    def __init__(self, society_code=None, number=None):
        self._society_code = society_code
        self._number = number