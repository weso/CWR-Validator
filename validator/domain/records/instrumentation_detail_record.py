from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INSTRUMENT_CODES
from validator.domain.records.record import Record


class InstrumentationDetailRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Instrument code', 'Number of players']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_alpha_regex(3), regex.get_numeric_regex(3, True)]

    def __init__(self, record):
        super(InstrumentationDetailRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Number of players')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'IND':
            raise FieldValidationError('IND record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Instrument code'] not in INSTRUMENT_CODES:
            raise FieldValidationError('Given instrument code: {} not in table'.format(
                self.attr_dict['Instrument code']))