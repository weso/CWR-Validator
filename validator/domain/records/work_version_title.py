from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.domain.records.record import Record


class WorkVersionTitle(Record):
    FIELD_NAMES = ['Record prefix', 'Original work title', 'ISWC of entire work', 'Language code',
                   'Writer one last name', 'Writer one first name', 'Source', 'Writer one CAE/IPI name ID',
                   'Writer one IPI base number', 'Writer two last name', 'Writer two first name',
                   'Writer two CAE/IPI name ID', 'Writer two IPI base number', 'Submitter work ID']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(60), regex.get_ascii_regex(11, True),
                   regex.get_alpha_regex(2, True), regex.get_ascii_regex(45, True), regex.get_ascii_regex(30, True),
                   regex.get_ascii_regex(60, True), regex.get_numeric_regex(11, True),
                   regex.get_numeric_regex(13, True), regex.get_ascii_regex(45, True), regex.get_ascii_regex(30, True),
                   regex.get_numeric_regex(11, True), regex.get_numeric_regex(13, True),
                   regex.get_ascii_regex(14, True)]

    def __init__(self, record):
        super(WorkVersionTitle, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Writer one IPI base number')
        self.format_integer_value('Writer two IPI base number')
        self.format_integer_value('Submitter work ID')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'VER':
            raise FieldValidationError('VER record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))
        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldValidationError('Given language code: {} not in table'.format(self.attr_dict['Language code']))