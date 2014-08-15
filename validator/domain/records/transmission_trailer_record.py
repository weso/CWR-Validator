__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.records.record import Record


class TransmissionTrailerRecord(Record):
    FIELD_NAMES = ['Record type', 'Group count', 'Transaction count', 'Record count']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'TRL'), regex.get_numeric_regex(5),
                   regex.get_numeric_regex(8), regex.get_numeric_regex(8)]

    def __init__(self, record):
        super(TransmissionTrailerRecord, self).__init__(record)

    def format(self):
        self.format_integer_value('Group count')
        self.format_integer_value('Transaction count')
        self.format_integer_value('Record count')

    def validate(self):
        pass

    def _validate_field(self, field_name):
        pass