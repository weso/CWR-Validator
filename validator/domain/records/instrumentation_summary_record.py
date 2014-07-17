from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import INSTRUMENTATION_CODES
from validator.domain.records.record import Record


class InstrumentationSummaryRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Number of voices', 'Standard instrumentation type', 'Instrumentation description']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_numeric_regex(3, True), regex.get_ascii_regex(3, True),
                   regex.get_ascii_regex(50, True)]

    def __init__(self, record):
        super(InstrumentationSummaryRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Number of voices')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'INS':
            raise FieldValidationError('INS record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Standard instrumentation type'] is not None:
            if self.attr_dict['Standard instrumentation type'] not in INSTRUMENTATION_CODES:
                raise FieldValidationError('Given instrumentation type: {} not in table'.format(
                    self.attr_dict['Standard instrumentation type']))