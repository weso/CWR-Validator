from validator.domain.exceptions.field_validation_error import FieldValidationError

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TIS_CODES
from validator.domain.records.record import Record
from validator.domain.values.record_prefix import RecordPrefix


class TerritoryRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Inclusion/Exclusion indicator', 'TIS numeric code']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_defined_values_regex(1, False, 'E', 'I'), regex.get_numeric_regex(4)]

    def __init__(self, record):
        super(TerritoryRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('TIS numeric code')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'TER':
            raise FieldValidationError('TER record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['TIS numeric code'] not in TIS_CODES:
            raise FieldValidationError('Given TIS code: {} not in table'.format(self.attr_dict['TIS numeric code']))