from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.cwr_utils.value_tables import WRITER_POSITIONS
from validator.domain.records.record import Record


class NROtherWriterRecord(Record):
    FIELD_NAMES = ['Record type', 'Writer name', 'Writer first name', 'Language code', 'Writer position']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(160), regex.get_ascii_regex(160),
                   regex.get_alpha_regex(2, True), regex.get_alpha_regex(1, True)]

    def __init__(self, record):
        super(NROtherWriterRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Writer position')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NOW':
            raise FieldValidationError('NOW record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldValidationError('Given language code: {} not in table'.format(self.attr_dict['Language code']))

        if self.attr_dict['Writer position'] is not None and 1 <= self.attr_dict['Writer position'] <= 2:
            raise FieldValidationError('Given writer position: {} must be 1 or 2'.format(
                self.attr_dict['Writer position']))