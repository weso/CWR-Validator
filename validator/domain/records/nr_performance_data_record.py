from validator.domain.exceptions.field_validation_error import FieldValidationError
from validator.domain.values.record_prefix import RecordPrefix

__author__ = 'Borja'
from validator.cwr_utils import regex
from validator.cwr_utils.value_tables import LANGUAGE_CODES
from validator.domain.records.record import Record


class NRPerformanceDataRecord(Record):
    FIELD_NAMES = ['Record prefix', 'Performing artist name', 'Performing artist first name',
                   'Performing artist IPI/CAE name ID', 'Performing artist IPI base number', 'Language code',
                   'Performance language', 'Performance dialect']

    FIELD_REGEX = [RecordPrefix.REGEX, regex.get_ascii_regex(160, True),regex.get_ascii_regex(160, True),
                   regex.get_ascii_regex(11, True), regex.get_ascii_regex(13, True), regex.get_alpha_regex(2, True),
                   regex.get_alpha_regex(2, True), regex.get_alpha_regex(3, True)]

    def __init__(self, record):
        super(NRPerformanceDataRecord, self).__init__(record)

    def format(self):
        self.attr_dict['Record prefix'] = RecordPrefix(self.attr_dict['Record prefix'])
        self.format_integer_value('Performing artist IPI base number')

    def validate(self):
        if self.attr_dict['Record prefix'].record_type != 'NPR':
            raise FieldValidationError('NPR record type expected, obtained {}'.format(
                self.attr_dict['Record prefix'].record_type))

        if self.attr_dict['Language code'] is not None and self.attr_dict['Language code'] not in LANGUAGE_CODES:
            raise FieldValidationError('Given language code: {} not in table'.format(self.attr_dict['Language code']))

        if self.attr_dict['Performance language'] is not None:
            if self.attr_dict['Performance language'] not in LANGUAGE_CODES:
                raise FieldValidationError('Given performance language: {} not in table'.format(
                    self.attr_dict['Performance language']))

        if self.attr_dict['Performing artist name'] is None:
            if self.attr_dict['Performance language'] is None:
                if self.attr_dict['Performance dialect'] is None:
                    raise FieldValidationError('Expected at least one of performing artist, language or dialect fields')