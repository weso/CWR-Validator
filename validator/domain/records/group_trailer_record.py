from validator.domain.exceptions.field_validation_error import FieldValidationError

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import CURRENCY_VALUES
from validator.domain.records.record import Record


class GroupTrailerRecord(Record):
    FIELD_NAMES = ['Record type', 'Group ID', 'Transaction count',
                   'Record count', 'Currency indicator', 'Total monetary value']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'GRT'), regex.get_numeric_regex(5),
                   regex.get_numeric_regex(8), regex.get_numeric_regex(8),
                   regex.get_alpha_regex(3, True), regex.get_numeric_regex(10, True)]

    def __init__(self, record):
        super(GroupTrailerRecord, self).__init__(record)

    def format(self):
        self.format_integer_value('Group ID')
        self.format_integer_value('Transaction count')
        self.format_integer_value('Record count')
        self.format_integer_value('Total monetary value')

    def validate(self):
        if self.attr_dict['Total monetary value'] is not None and self.attr_dict['Total monetary value'] > 0:
            if self.attr_dict['Currency indicator'] not in CURRENCY_VALUES:
                raise FieldValidationError('Given currency indicator: {} not in currency codes'.format(
                    self.attr_dict['Currency indicator']))