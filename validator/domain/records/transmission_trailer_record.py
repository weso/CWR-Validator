__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.records.record import Record


class TransmissionTrailer(Record):
    FIELD_NAMES = ['Record type', 'Group count', 'Transaction count', 'Record count']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'TRL'), regex.get_numeric_regex(5),
                   regex.get_numeric_regex(8), regex.get_numeric_regex(8)]

    def __init__(self, record):
        super(TransmissionTrailer, self).__init__(record)

    def _build_record(self, record):
        self.extract_value(0, 3)
        self.extract_integer_value(3, 5)
        self.extract_integer_value(8, 8)
        self.extract_integer_value(16, 8)

    def validate(self):
        pass