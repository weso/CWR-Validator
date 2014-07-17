__author__ = 'Borja'
from validator.cwr_utils import regex


class AviKey(object):
    SOCIETY_CODE = regex.get_numeric_regex(3, True)
    NUMBER = regex.get_ascii_regex(15, True)

    REGEX = '{}{}'.format(SOCIETY_CODE, NUMBER)

    def __init__(self, avikey=None):
        self.society_code = int(avikey[0:3])
        self.number = avikey[3:18]