__author__ = 'Borja'
from validator.cwr_utils import regex


class VIsan(object):
    VERSION = regex.get_numeric_regex(8, True)
    ISAN = regex.get_numeric_regex(12, True)
    EPISODE = regex.get_numeric_regex(4, True)
    CHECK_DIGIT = regex.get_numeric_regex(1, True)

    REGEX = '{0}{1}{2}{3}'.format(
        VERSION, ISAN, EPISODE, CHECK_DIGIT)

    def __init__(self, version=None, isan=None, episode=None, check_digit=None):
        self._version = version
        self._isan = isan
        self._episode = episode
        self._check_digit = check_digit