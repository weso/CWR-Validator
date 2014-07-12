__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.records.record import Record


class TransmissionTrailer(Record):
    FIELD_NAMES = ['Record type', 'Group count', 'Transaction count', 'Record count']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'TRL'), regex.get_numeric_regex(5),
                   regex.get_numeric_regex(8), regex.get_numeric_regex(8)]

    def __init__(self, record):
        super(TransmissionTrailer, self).__init__(record)

    def format(self):
        self._attr_dict['Group count'] = self.format_integer_value(self._attr_dict['Group count'])
        self.attr_dict['Transaction count'] = self.format_integer_value(self.attr_dict['Transaction count'])
        self.attr_dict['Record count'] = self.format_integer_value(self.attr_dict['Record count'])

    def validate(self):
        pass