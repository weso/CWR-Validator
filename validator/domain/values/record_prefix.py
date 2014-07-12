__author__ = 'Borja'
from validator.cwr_utils import regex


class RecordPrefix(object):
    RECORD_TYPE = regex.get_alpha_regex(3)
    TRANSACTION_NUMBER = regex.get_numeric_regex(8)
    RECORD_NUMBER = regex.get_numeric_regex(8)

    REGEX = regex.Regex('{}{}{}'.format(RECORD_TYPE, TRANSACTION_NUMBER, RECORD_NUMBER), 19)

    def __init__(self, prefix=None):
        self.record_type = prefix[0:3]
        self.transaction_number = int(prefix[3:11])
        self.record_number = int(prefix[11:19])