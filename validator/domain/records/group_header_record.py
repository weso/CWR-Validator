from validator.domain.exceptions.field_validation_error import FieldValidationError

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TRANSACTION_VALUES
from validator.domain.records.record import Record


class GroupHeaderRecord(Record):
    FIELD_NAMES = ['Record type', 'Transaction type', 'Group ID', 'Transaction type version number',
                   'Batch request', 'Submission/Distribution type']

    FIELD_REGEX = [regex.get_defined_values_regex(3, False, 'GRH'), regex.get_alpha_regex(3),
                   regex.get_numeric_regex(5), regex.get_defined_values_regex(5, False, '02\.10'),
                   regex.get_numeric_regex(10, True), regex.get_optional_regex(2)]

    def __init__(self, record):
        super(GroupHeaderRecord, self).__init__(record)

    def format(self):
        self.format_integer_value('Group ID')
        self.format_integer_value('Batch request')

    def validate(self):
        if self.attr_dict['Transaction type'] not in TRANSACTION_VALUES:
            raise FieldValidationError('Given transaction type: {} not in required ones'.format(self.attr_dict[
                "Transaction type"]))

        if self.attr_dict['Group ID'] > len(TRANSACTION_VALUES):
            raise FieldValidationError('Given group id: {} bigger than expected (00003)'.format(self.attr_dict[
                "Group ID"]))