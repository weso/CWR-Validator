from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.domain.records.record import Record


class WorkCompositeRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Title', 'ISWC of component', 'Submitter work ID', 'Duration',
                   'Writer one last name', 'Writer one first name', 'Writer one CAE/IPI name',
                   'Writer two last name', 'Writer two first name', 'Writer two CAE/IPI name',
                   'Writer one IPI base number', 'Writer two IPI base number']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(60), regex.get_ascii_regex(11, True),
                   regex.get_ascii_regex(14, True), regex.get_time_regex(True), regex.get_ascii_regex(45),
                   regex.get_ascii_regex(30, True), regex.get_numeric_regex(11, True), regex.get_ascii_regex(45, True),
                   regex.get_ascii_regex(30, True), regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True), regex.get_numeric_regex(13, True)]

    def __init__(self, record):
        super(WorkCompositeRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_time_value('Duration')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'COM':
            raise FieldValidationError('COM record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Writer two first name'] is not None and self.attr_dict['Writer two last name'] is None:
            raise FieldValidationError('Expected writer two last name as first name is entered')