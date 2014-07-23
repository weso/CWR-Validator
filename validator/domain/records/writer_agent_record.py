from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.records.record import Record


class WriterAgentRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Publisher IP ID', 'Publisher name', 'Submitter agreement number',
                   'Society assigned agreement number', 'Writer IP ID']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(9), regex.get_ascii_regex(45),
                   regex.get_ascii_regex(14, True), regex.get_ascii_regex(14, True), regex.get_ascii_regex(9)]

    def __init__(self, record):
        super(WriterAgentRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Submitter agreement number')
        self.format_integer_value('Society assigned agreement number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'PWR':
            raise FieldValidationError('PWR record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))