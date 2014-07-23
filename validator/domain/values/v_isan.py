__author__ = 'Borja'
from validator.cwr_utils import regex


class VIsan(object):
    VERSION = regex.get_numeric_regex(8, True)
    ISAN = regex.get_numeric_regex(12, True)
    EPISODE = regex.get_numeric_regex(4, True)
    CHECK_DIGIT = regex.get_numeric_regex(1, True)

    REGEX = regex.Regex('{}{}{}{}'.format(
        VERSION, ISAN, EPISODE, CHECK_DIGIT), 25)

    def __init__(self, visan=None):
        self.version = int(visan[0:7])
        self.isan = int(visan[7:19])
        self.episode = int(visan[19:23])
        self.check_digit = int(visan[23:24])