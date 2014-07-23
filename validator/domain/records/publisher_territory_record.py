from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import TIS_CODES
from validator.domain.records.record import Record


class PublisherTerritoryRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Interested party ID', 'Constant', 'PR collection share', 'MR collection share',
                   'SR collection share', 'Inclusion/Exclusion indicator', 'TIS numeric code', 'Shares change',
                   'Sequence ID']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(9), regex.get_optional_regex(6),
                   regex.get_numeric_regex(5, True), regex.get_numeric_regex(5, True), regex.get_numeric_regex(5, True),
                   regex.get_defined_values_regex(1, False, 'E', 'I'), regex.get_numeric_regex(4),
                   regex.get_boolean_regex(), regex.get_numeric_regex(3)]

    def __init__(self, record):
        super(PublisherTerritoryRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_float_value('PR collection share', 3)
        self.format_float_value('MR collection share', 3)
        self.format_float_value('SR collection share', 3)
        self.format_integer_value('TIS numeric code')
        self.format_integer_value('Sequence ID')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'SPT':
            raise FieldValidationError('SPT record type expected, obtained: {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['TIS numeric code'] not in TIS_CODES:
            raise FieldValidationError('Given TIS numeric code: {} not in table'.format(
                self.attr_dict['TIS numeric code']))

        if 0 > self.attr_dict['PR collection share'] or self.attr_dict['PR collection share'] > 50:
            raise FieldValidationError('Expected PR share between 0 and 50, obtained {}'.format(
                self.attr_dict['PR collection share']))

        if 0 > self.attr_dict['MR collection share'] or self.attr_dict['MR collection share'] > 100:
            raise FieldValidationError('Expected MR share between 0 and 100, obtained {}'.format(
                self.attr_dict['MR collection share']))

        if 0 > self.attr_dict['SR collection share'] or self.attr_dict['SR collection share'] > 100:
            raise FieldValidationError('Expected SR share between 0 and 100, obtained {}'.format(
                self.attr_dict['SR collection share']))